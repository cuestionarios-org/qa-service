from flask import Blueprint,request, jsonify
from app.services import CategoryService  # Asegúrate de implementar este servicio


category_bp = Blueprint('category', __name__)

# Rutas para las Categorías
@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all_categories()
    return jsonify(categories), 200

@category_bp.route('/', methods=['POST'])
def create_category():
    """
    Crea una nueva categoria.
    
    Se requiere un objeto con la siguiente estructura:
    {
        'name': str,
        'description': str
    }
    
    Devuelve el objeto de la categoria recien creada.
    
    :statuscode 201: Categoria creada exitosamente
    :statuscode 400: No se proporcionaron los datos necesarios
    """
    print("XXXXXXX Hola XXXXXXX")
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    required_fields = ['name', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    category = CategoryService.create_category(data)
    return jsonify(category), 201

@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    """
    Obtiene los detalles de una categoria.
    
    :param id: El id de la categoria a obtener
    :statuscode 200: Categoria encontrada exitosamente
    :statuscode 404: Categoria no encontrada
    """
    try:
        category = CategoryService.get_category(id)
        return jsonify(category), 200
    except LookupError:
        return jsonify({"msg": "Category not found"}), 404

@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = CategoryService.update_category(id, data)
    return jsonify(category)

@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    CategoryService.delete_category(id)
    return '', 204
