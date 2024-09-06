from enum import Enum
from typing import Literal, Union

from gen_ai_hub.orchestration.models.base import JSONSerializable


class ContentFilterProvider(str, Enum):
    """
    Enumerates supported content filter providers.

    This enum defines the available content filtering services that can be used
    for content moderation tasks. Each enum value represents a specific provider.

    Values:
        AZURE: Represents the Azure Content Safety service.
    """

    AZURE = "azure_content_safety"


class ContentFilter(JSONSerializable):
    """
    Base class for content filtering configurations.

    This class provides a generic structure for defining content filters
    from various providers. It allows for specifying the provider and
    associated configuration parameters.

    Args:
        provider: The name of the content filter provider.
        config: A dictionary containing the configuration parameters for the content filter.
    """

    def __init__(self, provider: Union[ContentFilterProvider, str], config: dict):
        self.provider = provider
        self.config = config

    def to_dict(self):
        return {"type": self.provider, "config": self.config}


class AzureContentFilter(ContentFilter):
    """
    Specific implementation of ContentFilter for Azure's content filtering service.

    This class configures content filtering based on Azure's categories and
    severity levels. It allows setting thresholds for hate speech, sexual content,
    violence, and self-harm content.

    The thresholds are set using severity levels ranging from 0 to 6.
    A lower level like 0 is stricter, while a higher level like 6 is more lenient.

    Args:
        hate: Threshold for hate speech content.
        sexual: Threshold for sexual content.
        violence: Threshold for violent content.
        self_harm: Threshold for self-harm content.
    """

    def __init__(
        self,
        hate: Literal[0, 2, 4, 6],
        sexual: Literal[0, 2, 4, 6],
        violence: Literal[0, 2, 4, 6],
        self_harm: Literal[0, 2, 4, 6],
        **kwargs
    ):
        super().__init__(
            provider=ContentFilterProvider.AZURE,
            config={
                "Hate": hate,
                "Sexual": sexual,
                "Violence": violence,
                "SelfHarm": self_harm,
                **kwargs,
            },
        )
