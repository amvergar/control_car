# /src/core/validators.py
from dataclasses import dataclass
from typing import Optional


class ValidationError(ValueError):
    """Error de validación de datos de entrada."""


def require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValidationError(f"{name} debe ser mayor que 0. Valor recibido: {value}")


def require_non_negative(name: str, value: float) -> None:
    if value < 0:
        raise ValidationError(f"{name} no puede ser negativo. Valor recibido: {value}")


def require_not_empty(name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValidationError(f"{name} no puede estar vacío.")


def require_greater(name_a: str, a: float, name_b: str, b: float) -> None:
    if a <= b:
        raise ValidationError(f"{name_a} debe ser mayor que {name_b}. {a} <= {b}")


@dataclass(frozen=True)
class PositiveFloat:
    """Objeto de valor que garantiza números positivos."""
    name: str
    value: float

    def __post_init__(self):
        require_positive(self.name, self.value)


@dataclass(frozen=True)
class NonNegativeFloat:
    """Objeto de valor que garantiza números >= 0."""
    name: str
    value: float

    def __post_init__(self):
        require_non_negative(self.name, self.value)
