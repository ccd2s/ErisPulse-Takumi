from dataclasses import dataclass, field

from ErisPulse.Core.Bases import BaseConfig


@dataclass
class TakumiConfig(BaseConfig):

    enabled: bool = field(
        default=True,
        metadata={
            "description": {"i18n": "Takumi.enabled", "default": "是否启用模块"},
        },
    )
