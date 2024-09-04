from typing import Dict, Optional

from thestage_core.services.config_provider.config_provider import ConfigProviderCore
from thestage_core.services.clients.thestage_api.api_client import TheStageApiClientCore
from thestage_core.entities.config_entity import ConfigEntity, MainConfigEntity


class ValidationServiceCore:
    _thestage_api_client: TheStageApiClientCore = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClientCore,
            config_provider: ConfigProviderCore,
    ):
        self._thestage_api_client = thestage_api_client
        self._config_provider = config_provider

    @staticmethod
    def is_present_token(config: ConfigEntity) -> bool:
        present_token = True
        if not config:
            present_token = False
        else:
            if not config.main.thestage_auth_token:
                present_token = False

            if config.start_on_daemon:
                if config.daemon and config.daemon.daemon_token:
                    present_token = True
                else:
                    present_token = False

        return present_token

    def validate_token(self, new_token: str,) -> bool:
        is_valid: bool = False
        if new_token:
            is_valid = self._thestage_api_client.validate_token(token=new_token)
        return is_valid
