import dataclasses


@dataclasses.dataclass
class Config:
    count_arg_name: str | None = "first"  # ToDo: Improve Unset
    count_missing_arg_value: int = 1
