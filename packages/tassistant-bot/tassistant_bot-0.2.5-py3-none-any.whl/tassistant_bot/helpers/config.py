import os
from typing import Optional, Dict, Type
from dotenv import dotenv_values, load_dotenv

load_dotenv()


class SingletonMeta(type):
    _instances: Dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(
        cls: Type["SingletonMeta"], *args: tuple, **kwargs: dict
    ) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self, env_file: str = ".env") -> None:
        self._env_file = env_file
        self._config: Dict[str, str] = dotenv_values(env_file)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._config.get(key, default)

    def set(self, key: str, value: str) -> None:
        """
        Sets the value for a given key in the configuration and updates the .env file.

        :param key: The key to set.
        :param value: The value to set.
        """
        self._config[key] = value
        self._update_env_file()

    def update(self, updates: Dict[str, str]) -> None:
        """
        Updates multiple key-value pairs in the configuration and updates the .env file.

        :param updates: A dictionary containing key-value pairs to update.
        """
        self._config.update(updates)
        self._update_env_file()

    def _update_env_file(self) -> None:
        """
        Writes the current configuration back to the .env file.
        """
        with open(self._env_file, "w") as f:
            for key, value in self._config.items():
                f.write(f"{key}={value}\n")


config = Config(env_file=os.path.join(os.getcwd(), ".env"))
