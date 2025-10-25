from __future__ import annotations

from wexample_config.const.types import DictConfig
from wexample_wex_addon_dev_python.workdir.python_package_workdir import PythonPackageWorkdir


class AppWorkdir(PythonPackageWorkdir):
    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        return raw_value
