# En un archivo llamado: dto/cliente_response_dto.py

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ClienteResponseDTO:
    """
    Representa los datos de un cliente que se envían como respuesta.
    Es el equivalente directo de la clase Java ClienteResponseDTO.

    La decoración @dataclass genera automáticamente métodos como __init__,
    similar a @Data de Lombok. `frozen=True` la hace inmutable.
    """
    id: int
    nombre: str
    apellido: str
    rfc: str
    correo: str
    telefono: Optional[str] # El teléfono puede ser opcional