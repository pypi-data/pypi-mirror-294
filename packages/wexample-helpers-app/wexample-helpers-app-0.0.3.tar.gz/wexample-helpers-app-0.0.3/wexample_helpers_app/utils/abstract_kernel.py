from typing import Any, Optional, Dict

from pydantic import BaseModel, Field
from wexample_helpers.const.types import StringsList
from wexample_prompt.io_manager import IOManager
from wexample_filestate.file_state_manager import FileStateManager


class AbstractKernel(BaseModel):
    io: Optional[IOManager] = None
    directory: Optional[FileStateManager] = None
    entrypoint_path: str = Field(description="The main file placed at application root directory")
    root_path: Optional[str] = None
    env_config: Dict[str, Optional[str]] = None
    expected_env_items: Optional[StringsList] = [
        "APP_ENV"
    ]

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)

        self.io = IOManager()

        import os
        self.root_path = os.path.dirname(os.path.realpath(self.entrypoint_path)) + os.sep
        # TODO Use a directory manager like
        # self.directory = (self.directory_structure_class)(path=root_path)

        self._init_env_values()
        self._check_env_values()

    def _init_env_values(self):
        from dotenv import dotenv_values

        self.env_config = dotenv_values(f"{self.root_path}.env")

    def _check_env_values(self):
        from wexample_helpers.helpers.dict_helper import dict_get_first_missing_key
        first_missing_key = dict_get_first_missing_key(self.env_config, self.expected_env_items)
        if first_missing_key:
            # TODO Use logger
            print('ERROR: Missing .env configuration ' + first_missing_key)
            exit()
