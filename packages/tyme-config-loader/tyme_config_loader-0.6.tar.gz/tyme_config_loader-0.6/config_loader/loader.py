import os
import json
from abc import abstractmethod
from functools import cache
from typing import Any
import yaml


class LoadConfigError(Exception):
    """
    Could not load config
    """


class LoadConfigOptionError(Exception):
    """The options parameter of load() config is not valid!"""


class ConfigManager:
    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        """Load config"""

    @classmethod
    @abstractmethod
    def load_by_key_elements(cls, cfg_key_el: list[str], **options) -> dict:
        """Load config
        Params:
            - cfg_key_el: list element to construct config key
            - options: load config options
        """

    @classmethod
    @abstractmethod
    def load_by_key(cls, cfg_key, **options) -> dict:
        """Load config
        Params:
            - cfg_key_el: list element to construct config key
            - options: load config options
        """


class FileConfigManager(ConfigManager):
    def __init__(self, cfg_prefix: str = None):
        self.cfg_prefix = cfg_prefix

    def construct_key_prefix(self, key_els: list[str]) -> str:
        if self.cfg_prefix is not None:
            return os.path.join(self.cfg_prefix, *key_els)
        else:
            return os.path.join(*key_els)

    def load_by_key_elements(self, cfg_key_el: list[str], **options) -> dict:
        if options == {}:
            options = {"type": "yml"}

        cfg_key_prx = self.construct_key_prefix(cfg_key_el)
        cfg_key = cfg_key_prx + f".{options.get('type')}"

        try:
            with open(cfg_key, "r") as fp:
                raw_content = fp.read()
                match options.get("type"):
                    case "json":
                        cfg = json.loads(raw_content)
                    case "yaml" | "yml":
                        cfg = yaml.safe_load(raw_content)
                    case _:
                        raise LoadConfigOptionError("Config type is not supported yet!")
                return cfg
        except FileNotFoundError as exc:
            raise LoadConfigError(
                f"Could not load config from file at `{cfg_key}`"
            ) from exc

    def load(cls, *args, **kwargs):
        config_key: str = kwargs.get("config_key")
        config_key_el: list[str] = kwargs.get("config_key_el")
        if config_key is not None:
            return cls.load_by_key(cfg_key=config_key)
        else:
            return cls.load_by_key_elements(cfg_key_el=config_key_el)

    def load_by_key(self, cfg_key: str, **options) -> dict:
        _, file_extension = os.path.splitext(cfg_key)
        if file_extension == "":
            file_extension = "yml"
            cfg_key += "." + file_extension
        else:
            file_extension = file_extension.replace(".", "")

        if self.cfg_prefix is not None:
            path = f"{self.cfg_prefix}/{cfg_key}"
        else:
            path = cfg_key
        try:
            with open(path, "r") as fp:
                raw_content = fp.read()
            match file_extension:
                case "yaml" | "yml":
                    cfg = yaml.safe_load(raw_content)
                case "json":
                    cfg = json.loads(raw_content)
                case _:
                    raise LoadConfigOptionError("Config type is not supported yet!")
            return cfg
        except FileNotFoundError as exc:
            raise LoadConfigError(
                f"Could not load config from file at `{path}`"
            ) from exc
