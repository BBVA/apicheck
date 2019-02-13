from dataclasses import dataclass, fields


@dataclass
class EndPointParam(object):
    name: str
    param_type: str
    description: str
    default: str
    minimum_value: str
    maximum_value: str
    max_length: int

    def __post_init__(self):
        params = [(f.name, f.type) for f in fields(self)]
        for p_name, p_type in params:
            if type(getattr(self, p_name)) is not p_type:
                raise ValueError(f"Invalid type for '{p_name}' property")

