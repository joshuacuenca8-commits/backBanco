# En un archivo llamado: dto/cliente_mapper.py

# --- Importaciones de nuestro proyecto ---
# Se asume que el modelo 'Cliente' está definido en esa ruta.
from ..model.cliente import Cliente
from typing import Optional

# En Python, los DTOs suelen ser diccionarios.
# ClienteRequestDTO sería un dict proveniente de un JSON.
# ClienteResponseDTO sería un dict que se convierte a JSON.


def to_entity(request_dto: dict) -> Optional[Cliente]:
    """
    Convierte un DTO de petición (diccionario) a una entidad del modelo Cliente.
    Equivalente a: public static Cliente toEntity(ClienteRequestDTO dto)
    """
    if request_dto is None:
        return None

    # Se crea una nueva instancia del modelo SQLAlchemy
    cliente = Cliente()

    # Se asignan los valores del diccionario al objeto.
    # Usar .get() es más seguro que el acceso directo, ya que devuelve None
    # si la clave no existe, en lugar de lanzar un error.
    cliente.nombre = request_dto.get('nombre')
    cliente.apellido = request_dto.get('apellido')
    cliente.rfc = request_dto.get('rfc')
    cliente.correo = request_dto.get('correo')
    cliente.telefono = request_dto.get('telefono')

    return cliente


def to_response(cliente: Cliente) -> Optional[dict]:
    """
    Convierte una entidad del modelo Cliente a un DTO de respuesta (diccionario).
    Equivalente a: public static ClienteResponseDTO toResponse(Cliente cliente)
    """
    if cliente is None:
        return None

    # Se crea el diccionario que se enviará como respuesta JSON.
    response_dto = {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "rfc": cliente.rfc,
        "correo": cliente.correo,
        "telefono": cliente.telefono
    }

    return response_dto