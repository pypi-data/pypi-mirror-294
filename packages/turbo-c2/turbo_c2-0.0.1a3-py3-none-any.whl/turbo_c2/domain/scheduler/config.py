from dataclasses import dataclass, field


prefix = "ebf"


@dataclass
class Config:
    central_api_identifier: str
    job_controller_state_machine_identifier: str
    default_group_path: str
    serve_host: str
    cors_origins: list[str]


@dataclass
class ModeConfig:
    mode: str


@dataclass
class DefaultConfig(Config, ModeConfig):
    central_api_identifier: str = f"{prefix}_central_api"
    job_controller_state_machine_identifier: str = "job_controller_state_machine"
    default_group_path: str = "root"
    mode: str = "remote"
    serve_host: str = "127.0.0.1"
    cors_origins: list[str] = field(default_factory=lambda: ["*"])
