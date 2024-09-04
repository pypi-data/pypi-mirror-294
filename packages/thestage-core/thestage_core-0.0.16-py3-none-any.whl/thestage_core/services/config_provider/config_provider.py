import json
import os
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, Dict, Any

import dotenv


from thestage_core.config import THESTAGE_CONFIG_DIR, THESTAGE_CONFIG_FILE, THESTAGE_AUTH_TOKEN, THESTAGE_API_URL, \
    THESTAGE_DAEMON_ENV_PATH, THESTAGE_DAEMON_TOKEN, THESTAGE_DAEMON_BACKEND
from thestage_core.services.filesystem_service import FileSystemServiceCore
from thestage_core.entities.config_entity import ConfigEntity, MainConfigEntity
from thestage_core.exceptions.file_system_exception import FileSystemException


class ConfigProviderCore:

    # path to current physical subject we work with (project / etc) - might be passed explicitly
    _local_path: Optional[Path] = None
    _local_config_path: Optional[Path] = None
    _global_config_path: Optional[Path] = None
    _global_config_file: Optional[Path] = None
    _file_system_service = FileSystemServiceCore

    def __init__(
            self,
            local_path: Optional[str] = None,
    ):
        self._file_system_service = FileSystemServiceCore()
        if local_path:
            self._local_path = self._file_system_service.get_path(directory=local_path, auto_create=False)

        self.__set_config_paths()
        self.__init_global_config()

    def __set_config_paths(self):
        config_folder_name = self._file_system_service.get_path(f"{THESTAGE_CONFIG_DIR}", False)
        self._local_config_path = self._local_path.joinpath(config_folder_name)

        home_dir = self._file_system_service.get_home_path()
        self._global_config_path = home_dir.joinpath(config_folder_name)

    def __init_global_config(self) -> None:
        if self._global_config_path:
            if not self._global_config_path.exists():
                self._file_system_service.create_if_not_exists(self._global_config_path)

        self._global_config_file = self._global_config_path.joinpath(
            self._file_system_service.get_path(f"{THESTAGE_CONFIG_FILE}", False)
        )
        if not self._global_config_file.exists():
            self._file_system_service.create_if_not_exists_file(self._global_config_file)

    @staticmethod
    def __read_data_from_env() -> Optional[Dict[str, Any]]:
        result = {}
        tsr_auth_token = THESTAGE_AUTH_TOKEN
        tsr_config_local_dir = THESTAGE_CONFIG_DIR
        tsr_config_api_url = THESTAGE_API_URL

        if tsr_auth_token:
            result = {}
            result['main'] = {}
            if tsr_auth_token:
                result['main']['thestage_auth_token'] = tsr_auth_token
            if tsr_config_local_dir:
                result['main']['thestage_config_local_dir'] = tsr_config_local_dir
            if tsr_config_api_url:
                result['main']['thestage_api_url'] = tsr_config_api_url

        return result

    def _read_config_file(self, path: Path) -> Dict[str, Any]:
        result = {}
        try:
            if path and path.exists():
                with path.open("r") as file:
                    try:
                        if os.stat(path).st_size != 0:
                            result = json.load(file)
                    except JSONDecodeError:
                        pass
        except OSError:
            raise FileSystemException("Error open local config file")
        return result

    @staticmethod
    def _save_config_file(data: Dict, file_path: Path):
        with open(file_path, 'w') as configfile:
            json.dump(data, configfile, indent=1)

    def __read_global_config(self, ) -> Dict[str, Any]:
        return self._read_config_file(self._global_config_file)

    @staticmethod
    def __update_config_values_dict(values_to_update: Dict, new_values: Dict):
        if 'main' in new_values:
            if 'main' in values_to_update:
                values_to_update['main'].update(new_values['main'])
            else:
                values_to_update['main'] = new_values['main']

    def get_full_config(self, check_daemon: bool = False,) -> ConfigEntity:
        config_values = {}

        # read env data
        config_from_env = self.__read_data_from_env()
        if config_from_env:
            self.__update_config_values_dict(values_to_update=config_values, new_values=config_from_env)

        # read global config data
        config_from_file = self.__read_global_config()
        if config_from_file:
            self.__update_config_values_dict(values_to_update=config_values, new_values=config_from_file)

        config = ConfigEntity.model_validate(config_values)

        if self._local_path:
            config.runtime.working_directory = str(self._local_path)
        if self._global_config_path and not config.runtime.config_global_path:
            config.runtime.config_global_path = str(self._global_config_path)

        if check_daemon:
            self.check_for_daemon(config=config)

        return config

    def create_runtime_config(
            self,
            token: Optional[str] = None,
            no_dialog: bool = False,
    ) -> ConfigEntity:

        config = self.get_full_config()
        if not (config.main and config.main.thestage_auth_token):
            config.main.thestage_auth_token = token

        if self._local_path:
            config.runtime.working_directory = str(self._local_path)

        return config

    def save_global_config(self, config: ConfigEntity):
        data = self.__read_global_config()
        data.update(config.model_dump(exclude_none=True, by_alias=True, exclude={'runtime', 'RUNTIME', 'daemon', 'DAEMON'}))
        self._save_config_file(data=data, file_path=self._global_config_file)

    def save_token_to_config(self, token: str):
        tmp_config = ConfigEntity()
        tmp_config.main = MainConfigEntity(
            thestage_auth_token=token,
        )

        self.save_global_config(tmp_config)

    def remove_all_config(self,):
        self.remove_global_config()
        self.remove_config_env()

    def remove_global_config(self,):
        if self._global_config_path and self._global_config_path.exists():
            self._file_system_service.remove_folder(str(self._global_config_path))

    @staticmethod
    def remove_config_env():
        os.unsetenv('THESTAGE_CONFIG_DIR')
        os.unsetenv('THESTAGE_CONFIG_FILE')
        os.unsetenv('THESTAGE_CLI_ENV')
        os.unsetenv('THESTAGE_API_URL')
        os.unsetenv('THESTAGE_LOG_FILE')
        os.unsetenv('THESTAGE_AUTH_TOKEN')

    @staticmethod
    def check_for_daemon(config: ConfigEntity,):
        daemon_env_path = Path(THESTAGE_DAEMON_ENV_PATH)
        if daemon_env_path.exists():
            daemon_config = dotenv.dotenv_values(daemon_env_path)
            token_path = daemon_config.get('JWT_PATH')
            backend_api_url = daemon_config.get('BACKEND_URL')
            if daemon_config and token_path:
                daemon_token_path = Path(token_path)
                if daemon_token_path.exists():
                    with open(token_path, 'r') as f:
                        daemon_token = f.readline()
                    if daemon_token:
                        config.daemon.daemon_token = daemon_token.strip().replace('\\n', '')
                        config.daemon.backend_api_url = backend_api_url.strip().replace('\\n', '') if backend_api_url else None
                        config.start_on_daemon = True
        else:
            # maybe start on container
            if THESTAGE_DAEMON_TOKEN and THESTAGE_DAEMON_BACKEND:
                config.daemon.daemon_token = THESTAGE_DAEMON_TOKEN.strip().replace('\\n', '')
                config.daemon.backend_api_url = THESTAGE_DAEMON_BACKEND.strip().replace('\\n', '')
                config.start_on_daemon = True

