from enum import Enum

class EngineTypeEnum(Enum):
    CHROME = 'Chrome'
    FIREFOX = 'Firefox'
    EDGE = 'Edge'

class BaseENV:
    """
        Base Environment Configuration
        """

    def __init__(self, base_url: str, engine_type: EngineTypeEnum = EngineTypeEnum.CHROME, is_headless: bool = False):
        """
        :param base_url: Base URL for the environment
        :param engine_type: Browser engine type
        :param is_headless: Whether to run in headless mode
        """
        self.base_url = base_url.rstrip('/')
        self.engine_type = engine_type
        self.is_headless = is_headless

    def __repr__(self):
        return (f"BaseEnv(base_url='{self.base_url}', "
                f"engine_type={self.engine_type.value}, "
                f"is_headless={self.is_headless})")