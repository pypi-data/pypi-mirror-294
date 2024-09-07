import logging
import typing

from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options, Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.theme import Theme

logging.getLogger(__name__)


class OverwriteConfigsConfig(Config):
    theme = config_options.Type(dict, default=None)


class OverwriteConfigsPlugin(BasePlugin[OverwriteConfigsConfig]):
    def __init__(self):
        self._logger = logging.getLogger("mkdocs.overwrite-configs")
        self._logger.setLevel(logging.INFO)

    def _merge_theme(self, config: MkDocsConfig, theme: dict):
        if "theme" not in config:
            config.theme = Theme()
            self._logger.info("Theme not found in config, creating new theme")
            config.theme.update(theme)
        else:
            self._logger.info("Theme found in config, updating theme")
            config.theme.update(theme)
            self._logger.info("Theme updated")

    def on_config(self, config: MkDocsConfig):
        theme = self.config.theme
        self._merge_theme(config, theme)
        return config
