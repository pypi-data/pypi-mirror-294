import os

from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.options_values.content_filter.trim_content_filter import TrimContentFilter
from wexample_filestate.options_values.content_option_value import ContentOptionValue
from wexample_helpers.const.types import *

from wexample_wex_addon_app.const.globals import (
    APP_FILE_APP_CONFIG,
    APP_FILE_APP_ENV,
)
from wexample_wex_addon_app.options_values.readme_content_option_value import ReadmeContentOptionValue
from wexample_wex_core.utils.workdir import Workdir


class AppDirectoryStructure(Workdir):
    def build_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        config = super().build_config(config)
        children = config["children"]

        children.append({
            "name": 'README.md',
            "type": DiskItemType.FILE,
            "should_exist": True,
            "default_content": ReadmeContentOptionValue(
                templates=[],
                parameters={}
            ),
        })

        children.append({
            "name": 'version.txt',
            "type": DiskItemType.FILE,
            "should_exist": True,
            "default_content": f"0.0.1",
            "content": ContentOptionValue(filters=[TrimContentFilter()])
        })

        return config or {}

    def build_setup_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        config = super().build_setup_config(config)
        children = config["children"]

        children.append({
            "name": APP_FILE_APP_CONFIG,
            "type": DiskItemType.FILE,
            "should_exist": True
        })

        children.append({
            "name": APP_FILE_APP_ENV,
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
        })

        children.append({
            "name": "tmp",
            "type": DiskItemType.DIRECTORY,
            "should_exist": True
        })

        return config
