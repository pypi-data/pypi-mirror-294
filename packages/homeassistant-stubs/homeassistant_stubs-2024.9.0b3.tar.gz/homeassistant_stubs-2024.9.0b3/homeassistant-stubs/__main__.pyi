import argparse
from .const import REQUIRED_PYTHON_VER as REQUIRED_PYTHON_VER, RESTART_EXIT_CODE as RESTART_EXIT_CODE, __version__ as __version__

FAULT_LOG_FILENAME: str

def validate_os() -> None: ...
def validate_python() -> None: ...
def ensure_config_path(config_dir: str) -> None: ...
def get_arguments() -> argparse.Namespace: ...
def check_threads() -> None: ...
def main() -> int: ...
