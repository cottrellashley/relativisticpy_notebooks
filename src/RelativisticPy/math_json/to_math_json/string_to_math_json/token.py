from dataclasses import dataclass
from src.RelativisticPy.math_json.to_math_json.string_to_math_json.types import TokenType


@dataclass
class Token:
    type: TokenType
    value: any

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")