import dataclasses


@dataclasses.dataclass(frozen=True)
class Config:
    count_arg_name: str = "first"
    count_missing_arg_value: int = 1
