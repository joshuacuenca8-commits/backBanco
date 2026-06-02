# En un archivo que podría llamarse: dto/cliente_request_dto.py

from dataclasses import dataclass
import re # Importamos el módulo de expresiones regulares para validar el email

@dataclass(frozen=True)
class ClienteRequestDTO:
    """
    Representa y valida los datos de entrada para crear o actualizar un cliente.
    Es el equivalente directo de la clase Java ClienteRequestDTO.

    La decoración @dataclass genera automáticamente métodos como __init__ y __repr__,
    similar a @Data de Lombok. `frozen=True` la hace inmutable.
    """
    nombre: str
    apellido: str
    rfc: str
    correo: str
    telefono: str

    def __post_init__(self):
        """
        Este método es llamado automáticamente por la dataclass después de la inicialización.
        Lo usamos para realizar las validaciones, equivalente a las anotaciones de Jakarta.
        """
        # Validación para @NotBlank
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacio")
        if not self.apellido or not self.apellido.strip():
            raise ValueError("El apellido no puede estar vacio")
        if not self.rfc or not self.rfc.strip():
            raise ValueError("El rfc no puede estar vacio")
        if not self.correo or not self.correo.strip():
            raise ValueError("El correo no puede estar vacio")
        if not self.telefono or not self.telefono.strip():
            raise ValueError("El telefono no puede estar vacio")

        # Validación para @Email
        # Usamos una expresión regular simple para verificar el formato del correo.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.correo):
            raise ValueError("El correo debe de tener un formato valido")
        