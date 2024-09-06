from typing import Optional, List

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filter import ContentFilter
from gen_ai_hub.orchestration.models.llm import LLM
from gen_ai_hub.orchestration.models.template import Template


class OrchestrationConfig(JSONSerializable):
    """
    Configuration for the Orchestration Service's content generation process.

    Defines modules for a harmonized API that combines LLM-based content generation
    with additional processing functionalities. The service processes inputs
    through templates, LLMs, and optional content filters.

    Args:
        template: Template object for rendering input prompts.
        llm: Language model for text generation.
        input_filters: Filters applied to inputs. Defaults to an empty list.
        output_filters: Filters applied to outputs. Defaults to an empty list.
    """

    def __init__(
        self,
        template: Template,
        llm: LLM,
        input_filters: Optional[List[ContentFilter]] = None,
        output_filters: Optional[List[ContentFilter]] = None,
    ):
        self.template = template
        self.llm = llm
        self.input_filters = input_filters or []
        self.output_filters = output_filters or []

    def to_dict(self):
        config = {
            "module_configurations": {
                "templating_module_config": self.template.to_dict(),
                "llm_module_config": self.llm.to_dict(),
            }
        }

        filtering_config = {}

        if self.input_filters:
            filtering_config["input"] = {
                "filters": [f.to_dict() for f in self.input_filters]
            }

        if self.output_filters:
            filtering_config["output"] = {
                "filters": [f.to_dict() for f in self.output_filters]
            }

        if filtering_config:
            config["module_configurations"][
                "filtering_module_config"
            ] = filtering_config

        return config
