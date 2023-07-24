from pydantic import Field


def validate_length(
    cls: type,
    value: str,
    field: Field,  # type: ignore
    min_len: int,
    max_len: int,
) -> str:
    default_string = value.strip()
    if len(default_string) > max_len:
        raise ValueError(
            f"{field.alias} cannot exceed {max_len} characters",  # type: ignore
        )
    if len(default_string) < min_len:
        raise ValueError(
            f"{field.alias} cannot be less {min_len} characters",  # type: ignore
        )
    return default_string


def validate_attractiveness_scale(
    cls: type,
    value: int,
) -> int:
    try:
        value = int(value)
    except ValueError:
        raise ValueError("attractiveness_scale must be integer")
    if value < 1 or value > 5:
        raise ValueError("attractiveness_scale must be in range 1..5")

    return value
