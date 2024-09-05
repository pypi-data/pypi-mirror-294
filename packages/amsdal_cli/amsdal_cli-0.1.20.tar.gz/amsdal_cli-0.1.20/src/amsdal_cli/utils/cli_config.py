import re
from pathlib import Path

from pydantic import BaseModel
from pydantic import model_validator

from amsdal_cli.utils.vcs.enum import VCSOptions

APPLCATION_UUID_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9]{31}$')


class CliConfig(BaseModel):
    templates_path: Path
    config_path: Path = Path('/dev/null')
    http_port: int = 8080
    check_model_exists: bool = True
    application_uuid: str | None = None
    application_name: str | None = None
    json_indent: int = 4
    app_directory: Path = Path('/dev/null')
    verbose: bool = True
    vcs: VCSOptions | None = None

    @model_validator(mode='after')
    def validate_config_path(self) -> 'CliConfig':
        if self.app_directory == Path('/dev/null'):
            return self

        full_config_path: Path = self.app_directory / self.config_path
        self.config_path = full_config_path

        if self.application_uuid and not APPLCATION_UUID_PATTERN.match(self.application_uuid):
            msg = (
                f'The application_uuid "{self.application_uuid}" should match the '
                f'pattern "{APPLCATION_UUID_PATTERN.pattern}".'
            )
            raise ValueError(msg)

        if not full_config_path.exists():
            msg = f'The "{full_config_path}" does not exists. Check ".amdsal-cli -> config_path".'
            raise ValueError(msg)

        return self
