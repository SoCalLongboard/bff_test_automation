from typing import Tuple, Dict, Callable, Any

CliCommand = Dict[str, Tuple[str, Dict[str, Any]]]
CliSubCommand = Tuple[str, str, str, CliCommand, Callable]
