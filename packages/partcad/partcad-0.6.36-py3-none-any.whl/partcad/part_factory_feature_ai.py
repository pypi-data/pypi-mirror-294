#
# OpenVMP, 2024
#
# Author: Roman Kuzmenko
# Created: 2024-03-23
#
# Licensed under Apache License, Version 2.0.
#

import asyncio

import copy
import os
import tempfile
import threading

from .ai import Ai
from . import logging as pc_logging
from . import sync_threads as pc_thread
from .utils import total_size
from .user_config import user_config

DEFAULT_ALTERNATIVES_GEOMETRIC_MODELING = 3
DEFAULT_ALTERNATIVES_MODEL_GENERATION = 3
DEFAULT_INCREMENTAL_SCRIPT_CORRECTION = 2


class PartFactoryFeatureAi(Ai):
    """Used by all part factories that generate parts with GenAI."""

    LANG_PYTHON = "Python"

    part_type: str
    script_type: str
    prompt_suffix: str

    def __init__(self, config, part_type, script_type, prompt_suffix=""):
        self.part_type = part_type
        self.script_type = script_type
        self.prompt_suffix = prompt_suffix

        desc = config.get("desc", None)
        if desc is None:
            error = "%s: Prompt is not set" % config["name"]
            pc_logging.error(error)
            raise Exception(error)

        self.ai_config = copy.deepcopy(config)
        if "numGeometricModeling" in self.ai_config:
            self.num_geometric_modling = self.ai_config["numGeometricModeling"]
        else:
            self.num_geometric_modeling = (
                DEFAULT_ALTERNATIVES_GEOMETRIC_MODELING
            )
        if (
            user_config.max_geometric_modeling is not None
            and self.num_geometric_modeling > user_config.max_geometric_modeling
        ):
            self.num_geometric_modeling = user_config.max_geometric_modeling

        if "numModelGeneration" in self.ai_config:
            self.num_model_generation = self.ai_config[("numModelGeneration")]
        else:
            self.num_model_generation = DEFAULT_ALTERNATIVES_MODEL_GENERATION
        if (
            user_config.max_model_generation is not None
            and self.num_model_generation > user_config.max_model_generation
        ):
            self.num_model_generation = user_config.max_model_generation

        if "numScriptCorrection" in self.ai_config:
            self.num_script_correction = self.ai_config[("numScriptCorrection")]
        else:
            self.num_script_correction = DEFAULT_INCREMENTAL_SCRIPT_CORRECTION
        if (
            user_config.max_script_correction is not None
            and self.num_script_correction > user_config.max_script_correction
        ):
            self.num_script_correction = user_config.max_script_correction

        if not "tokens" in self.ai_config:
            self.ai_config["tokens"] = 2000

        # Use `temperature` and `top_p` values recommended for code generation
        # if no other preferences are set
        if not "temperature" in self.ai_config:
            self.ai_config["temperature"] = 0.2
        if not "top_p" in self.ai_config:
            self.ai_config["top_p"] = 0.1

    def on_init_ai(self):
        """This method must be executed at the very end of the part factory
        constructor to finalize the AI initialization. At the time of the call
        self.part and self.instantiate must be already defined."""
        self.part.generate = lambda path: self._create_file(path)

        # If uncommented out, this makes the package initialization
        # unaccceptably slow
        # if (
        #     not os.path.exists(self.config["path"])
        #     or os.path.getsize(self.config["path"]) == 0
        # ):
        #     self._create_file()
        self.instantiate_orig = self.instantiate
        self.instantiate = self._instantiate_ai

    async def _instantiate_ai(self, part):
        """This is a wrapper for the instantiate method that ensures that
        the part is (re)generated before the instantiation."""
        if not os.path.exists(part.path) or os.path.getsize(part.path) == 0:
            self._create_file(part.path)

        return await self.instantiate_orig(part)

    def _create_file(self, path):
        """This method is called to (re)generate the part."""

        # Geometric modeling
        modeling_options = []
        max_models = self.num_geometric_modeling
        max_tries = 2 * max_models

        # TODO(clairbee): Multiple AI calls are a good candidate to paralelize,
        #                 however it's useless without a paid subscription
        #                 with huge quotas. De-prioritized for now.
        #
        # def modeling_task():
        #     modeling_options.extend(self._geometric_modeling())
        # threads = []
        # for _ in range(NUM_ALTERNATIVES_GEOMETRIC_MODELING):
        #     thread = threading.Thread(target=modeling_task)
        #     thread.start()
        #     threads.append(thread)
        # for thread in threads:
        #     thread.join()

        tries = 0
        while len(modeling_options) < max_models and tries < max_tries:
            modeling_options.extend(self._geometric_modeling())
            pc_logging.info(
                "Generated %d geometric modeling candidates"
                % len(modeling_options)
            )
            tries += 1

        # For each remaining geometric modeling option,
        # generate a model and render an image
        script_candidates = []
        candidate_id = 0
        for modeling_option_idx, modeling_option in enumerate(modeling_options):
            pc_logging.debug(
                "Generated the geometric modeling candidate %d: %s"
                % (modeling_option_idx, modeling_option)
            )

            # Generate the models using the required language
            scripts = self._generate_script(modeling_option)

            for script in scripts:
                pc_logging.debug(
                    "Generated the script candidate %d: %s"
                    % (candidate_id, script)
                )

                # Validate the image by rendering it,
                # attempt to correct the script if rendering doesn't work
                image_filename, script = self._validate_and_fix(
                    modeling_option, script, candidate_id
                )
                # Check if the model was valid
                if image_filename is not None:
                    # Record the valid model and the image
                    script_candidates.append((image_filename, script))

                candidate_id += 1

            pc_logging.info(
                "So far %d valid script candidates" % len(script_candidates)
            )

        if len(script_candidates) == 0:
            pc_logging.error(
                "No valid script generated. Try changing the prompt."
            )
            return

        if len(script_candidates) == 1:
            script = script_candidates[0][1]
        else:
            # Compare the images and select the best one
            script = self.select_best_image(script_candidates)

        if not script is None:
            f = open(path, "w")
            f.write(script)
            f.close()

    def _geometric_modeling(self):
        """This method generates geometric modeling options for the part."""

        prompt = (
            """You are an engineer performing geometric modeling of mechanical parts.
Given a short verbal description of a part,
you are creating a detailed description of the geometric shapes
required to reproduce that part.
Create a detailed listing of all geometric shapes and how they are
located against each other
(including dimensions, distances and offset in millimeters,
and angles in degrees),
to reproduce the part with the following description:
%s
"""
            % self.ai_config["desc"]
        )

        if "properties" in self.config:
            properties = "\n".join(
                [
                    "  %s: %s" % (k, v)
                    for k, v in self.config["properties"].items()
                ]
            )
            prompt += (
                """

The part is further described by the following properties:
%s
"""
                % properties
            )

        image_filenames = self.ai_config.get("images", [])
        if len(image_filenames) > 0:
            prompt += """
            
The part is further described by the attached images.
"""

        options = self.generate(
            "Geometric",
            self.project.name,
            self.name,
            prompt,
            self.ai_config,
            self.num_geometric_modeling,
            image_filenames=image_filenames,
        )
        return options

    def _generate_script(self, geometric_modeling):
        """This method generates a script given specific geometric modeling."""

        prompt = """You are an AI assistant in an engineering department.
You are helping engineers to create programmatic scripts that produce CAD geometry data
for parts, mechanisms, buildings or anything else.
The scripts you create a fully functional and can be used right away, as is, in automated workflows.
Assume that the scripts you produce are used automatically to render 3D models and to validate them.
This time you are asked to generate a %s to define a 3D model of a part defined by
the following geometric modeling:
        %s
        """ % (
            self.script_type,
            geometric_modeling,
        )

        image_filenames = self.ai_config.get("images", [])
        if len(image_filenames) > 0:
            prompt += """
            
The part is further described by the attached images.
"""

        prompt += """%s

IMPORTANT: Output the %s itself and do not add any text or comments before or after it.
""" % (
            self.prompt_suffix,
            self.script_type,
        )

        scripts = self.generate(
            "Script",
            self.project.name,
            self.name,
            prompt,
            self.ai_config,
            image_filenames=image_filenames,
        )

        # Sanitize the output to remove the decorations
        scripts = list(map(lambda s: self._sanitize_script(s), scripts))

        return scripts

    def _sanitize_script(self, script: str):
        """Cleans up the GenAI output to keep the code only."""

        # Extract the first block between ``` if any
        loc_1 = script.find("```")
        loc_2 = script[loc_1 + 1 :].find("```") + loc_1
        if loc_2 > 0:
            # Note: the first ``` (and whatever follows on the same line) is still included
            script = script[loc_1:loc_2]

        # Remove ```` if anything is left
        script = "\n".join(
            list(
                filter(
                    lambda l: (
                        False
                        if l.startswith("```") or l.startswith(" ```")
                        else True
                    ),
                    script.split("\n"),
                )
            )
        )

        if hasattr(self, "lang") and self.lang == self.LANG_PYTHON:
            # Strip straight to the import statements (for AIs that don't ```)
            if script.startswith("from "):
                loc_from = 0
            else:
                loc_from = script.find("\nfrom ")
            if script.startswith("import "):
                loc_import = 0
            else:
                loc_import = script.find("\nimport ")

            if loc_from != -1 and loc_import != -1:
                loc = min(loc_import, loc_from)
            elif loc_from != -1:
                loc = loc_from
            else:
                loc = loc_import

            if loc != -1:
                script = script[loc:]

        return script

    def _validate_and_fix(self, modeling_option, script, candidate_id, depth=0):
        """
        Validate the image by rendering it,
        attempt to correct the script if rendering doesn't work.
        """
        next_depth = depth + 1

        # Render this script into an image.
        # We can't just stop at validating geometry,
        # as we need to feed the picture into the following AI logic.
        image_filename, error_text = self._render_image(script, candidate_id)
        if image_filename is not None:
            return image_filename, script
        # Failed to render the image.

        if next_depth <= self.num_script_correction:
            # Ask AI to make incremental fixes based on the errors.
            correction_candidate_id = 0
            for _ in range(self.num_script_correction):
                corrected_scripts = self._correct_script(
                    modeling_option, script, error_text
                )
                corrected_scripts = list(
                    map(lambda s: self._sanitize_script(s), corrected_scripts)
                )
                for corrected_script in corrected_scripts:
                    pc_logging.debug(
                        "Corrected the script candidate %d, correction candidate %d at depth %d: %s"
                        % (
                            candidate_id,
                            correction_candidate_id,
                            depth,
                            corrected_script,
                        )
                    )

                    image_filename, corrected_script = self._validate_and_fix(
                        modeling_option,
                        corrected_script,
                        candidate_id,
                        next_depth,
                    )
                    if image_filename is not None:
                        return image_filename, corrected_script

                    correction_candidate_id += 1

        return None, script

    def _correct_script(self, modeling_option, script, error_text):
        # TODO(clairbee): prove that the use of geometric modeling product
        #                 in this prompt is benefitial
        prompt = """You are an AI assistant to a mechanical engineer.
You are given an automatically generated %s which has flaws that need to be
corrected.

The generated script that contains errors is (until SCRIPT_END):
```
%s
```
SCRIPT_END

When the given script is executed, the following error messages are
produced (until ERRORS_END):
%s
ERRORS_END

Please, generate a corrected script so that it does not produce the given errors.
Make as little changes as possible and prefer not to make any changes that are
not necessary to fix the errors.
Very important not to produce exactly the same script: at least something has to change.
""" % (
            self.script_type,
            script,
            error_text,
        )

        pc_logging.debug("Correction prompt: %s" % prompt)

        options = self.generate(
            "ScriptIncr",
            self.project.name,
            self.name,
            prompt,
            self.ai_config,
            self.num_script_correction,
        )
        return options

    def _render_image(self, script, candidate_id):
        """This method ensures the validity of a script candidate by attempting to render it."""
        error_text = ""
        exception_text = ""

        source_path = tempfile.mktemp(suffix=self.extension)
        with open(source_path, "w") as f:
            f.write(script)
            f.close()
        pc_logging.debug("Generated script: %s" % source_path)

        output_path = tempfile.mktemp(suffix=".png")
        pc_logging.debug("Attempting to render: %s" % output_path)

        # Create an ephemeral part for the given script candidate
        part = self._create_part(
            {
                "name": self.name + "_candidate_" + str(candidate_id),
                # "path": source_path, # TODO(clairbee): doesn't this work? why?
                "type": self.part_type,
                "mute": True,  # Suppress errors
            }
        )
        # Since this is an ephemeral part, certain things need to be tweaked
        part.instantiate = self.instantiate_orig  # Remove the AI wrapper
        part.path = source_path  # Set the path to the temporary script file
        pc_logging.debug("Part created: %.2f KB" % (total_size(part) / 1024.0))

        def render(part):
            nonlocal exception_text
            try:
                coro = part.get_shape()
                with pc_logging.Action(
                    "Instantiate", part.project_name, part.name
                ):
                    shape = asyncio.run(coro)
                if not shape is None:
                    part.render_png(self.ctx, None, output_path)
            except Exception as e:
                part.error("Failed to render the image: %s" % e)
                exception_text += f"Exception:\n{str(e)}\n"

        # TODO(clairbee): make it async up until this point, drop threads
        # Given we don't know whether the current thread is already
        # running an event loop or not, we need to create a new thread
        t = threading.Thread(target=render, args=[part])
        t.start()
        t.join()

        errors = part.errors  # Save the errors
        errors = list(
            filter(
                lambda e: "Exception while deserializing" not in e,
                errors,
            )
        )
        if len(errors) > 0:
            pc_logging.debug(
                "There were errors while attemtping to render the image"
            )
            pc_logging.debug("%s" % errors)
            for error in errors:
                error_text += f"{error}\n"

        error_text = error_text + exception_text
        os.unlink(source_path)
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            pc_logging.info(
                "Script candidate %d: failed to render the image" % candidate_id
            )
            return None, error_text
        pc_logging.info(
            "Script candidate %d: successfully rendered the image"
            % candidate_id
        )
        return output_path, error_text

    def select_best_image(self, script_candidates):
        """Iterate over script_candidates and compare images.
        Each script candidate is [<image_filename>, <script>]."""

        if len(script_candidates) == 0:
            return None

        image_filenames = list(map(lambda c: c[0], script_candidates))

        prompt = (
            """
From the attached images, select the image that is the best fit
for the following description:
%s

Respond with the numeric index (starting with 1) of the best fit image.
No other text is acceptable.
Just the number.
"""
            % self.ai_config["desc"]
        )

        # Ask AI to compare the images
        pc_logging.info(
            "Attempting to select the best script by comparing images"
        )
        responses = self.generate(
            "Compare",
            self.project.name,
            self.name,
            prompt,
            self.ai_config,
            1,
            image_filenames=image_filenames,
        )

        pc_logging.debug("Image comparison responses: %s" % responses)

        # Parse the response to get the number out
        for response in responses:
            words = response.split(" ")
            words = list(filter(lambda w: w.strip().isnumeric(), words))
            if len(words) == 1:
                idx = int(words[0])
                if idx > 0 and idx <= len(script_candidates):
                    pc_logging.info("Selected the best fit image: %d" % idx)
                    return script_candidates[idx - 1][1]

        return script_candidates[0][1]
