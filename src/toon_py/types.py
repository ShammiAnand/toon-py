from dataclasses import dataclass
from typing import Literal


@dataclass
class EncodeOptions:
    indent: int = 2
    delimiter: Literal[",", "\t", "|"] = ","
    length_marker: Literal["#", False] = False
