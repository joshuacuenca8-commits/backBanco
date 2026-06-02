# En un archivo llamado: controller/cliente_controller.py

import logging
from flask import Blueprint, request, jsonify

# --- Importaciones de nuestro proyecto ---
# Suponiendo que la estructura del proyecto es similar a la que se muestra
# en la respuesta anterior.
from ..service.cliente_service import ClienteService
from ..dto.cliente_dto import cliente_to_response_dto
from ..exception.cliente_exceptions import ClienteNotFoundException

# Configuración del logger
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Blueprint para agrupar las rutas de clientes bajo /api/v1/clientes
cliente_bp = Blueprint('cliente_bp', __name__)

# Instancia del servicio que contiene la lógica de negocio
# En una aplicación más compleja, esto se manejaría con inyección de dependencias.
cliente_service = ClienteService()

# --- Definición de las rutas (endpoints) ---

# Equivalente a @GetMapping
@cliente_bp.route('/', methods=['GET'])
def obtener_clientes():
    """
    Obtener todos los clientes.
    Corresponde a: @Operation(summary = "Obtener todos los clientes")
    """
    log.info("GET /api/v1/clientes - obtener listado de clientes")
    # El servicio obtiene los clientes de la base de datos
    clientes = cliente_service.obtener_todos()
    # Convertimos cada objeto Cliente a un DTO (diccionario) para la respuesta
    response_dtos = [cliente_to_response_dto(c) for c in clientes]
    return jsonify(response_dtos), 200

# Equivalente a @GetMapping("/{id}")
@cliente_bp.route('/<int:id>', methods=['GET'])
def obtener_cliente_id(id):
    """
    Obtener cliente por ID.
    Corresponde a: @Operation(summary = "Obtener cliente por ID")
    """
    log.info(f"GET /api/v1/clientes/{id} - obtener cliente por ID")
    # El manejo de ClienteNotFoundException se hace en el manejador de errores global
    cliente = cliente_service.obtener_por_id(id)
    return jsonify(cliente_to_response_dto(cliente)), 200

# Equivalente a @PostMapping
@cliente_bp.route('/', methods=['POST'])
def crear_cliente():
    """
    Crear nuevo cliente.
    Corresponde a: @Operation(summary = "Crear nuevo cliente")
    """
    log.info("POST /api/v1/clientes - crear nuevo cliente")
    # @RequestBody es reemplazado por request.get_json()
    request_dto = request.get_json()

    # La validación (@Valid) se haría aquí, por ejemplo:
    if not request_dto or not all(k in request_dto for k in ('nombre', 'apellido', 'rfc', 'correo')):
        return jsonify({"error": "Datos inválidos o incompletos"}), 400

    # El DTO (diccionario) se pasa al servicio para crear la entidad
    cliente_creado = cliente_service.crear_cliente(request_dto)

    # Se retorna el nuevo cliente con el código de estado 201 (Created)
    return jsonify(cliente_to_response_dto(cliente_creado)), 201

# Equivalente a @PutMapping("/{id}")
@cliente_bp.route('/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    """
    Actualizar cliente.
    Corresponde a: @Operation(summary = "Actualizar cliente")
    """
    log.info(f"PUT /api/v1/clientes/{id} - actualizar cliente")
    request_dto = request.get_json()

    # La validación se puede hacer aquí también
    if not request_dto:
        return jsonify({"error": "Cuerpo de la petición vacío"}), 400

    cliente_actualizado = cliente_service.actualizar_cliente(id, request_dto)
    return jsonify(cliente_to_response_dto(cliente_actualizado)), 200

# Equivalente a @DeleteMapping("/{id}")
@cliente_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    """
    Eliminar cliente.
    Corresponde a: @Operation(summary = "Eliminar cliente")
    """
    log.info(f"DELETE /api/v1/clientes/{id} - eliminar cliente")
    cliente_service.eliminar_cliente(id)
    # ResponseEntity.noContent() es un cuerpo vacío con estado 204
    return '', 204

# Equivalente a @GetMapping("/rfc/{rfc}")
@cliente_bp.route('/rfc/<string:rfc>', methods=['GET'])
def buscar_por_rfc(rfc):
    """
    Buscar cliente por RFC.
    Corresponde a: @Operation(summary = "Buscar cliente por RFC")
    """
    log.info(f"GET /api/v1/clientes/rfc/{rfc} - buscar por RFC")
    # El servicio puede devolver None si no encuentra el cliente
    cliente = cliente_service.buscar_por_rfc(rfc)
    if cliente:
        return jsonify(cliente_to_response_dto(cliente)), 200
    else:
        # Lanzamos la excepción para que el manejador global la capture
        raise ClienteNotFoundException(f"Cliente con RFC {rfc} no encontrado")

# Equivalente a @GetMapping("/correo/{correo}")
@cliente_bp.route('/correo/<string:correo>', methods=['GET'])
def buscar_por_correo(correo):
    """
    Buscar cliente por correo.
    Corresponde a: @Operation(summary = "Buscar cliente por correo")
    """
    log.info(f"GET /api/v1/clientes/correo/{correo} - buscar por correo")
    cliente = cliente_service.buscar_por_correo(correo)
    if cliente:
        return jsonify(cliente_to_response_dto(cliente)), 200
    else:
        raise ClienteNotFoundException(f"Cliente con correo {correo} no encontrado")
    