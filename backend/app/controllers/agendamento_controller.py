from flask import Blueprint, jsonify, request
from app.services import agendamento_service
from flask_jwt_extended import jwt_required, get_jwt_identity

agendamento_bp = Blueprint('agendamentos', __name__)

@agendamento_bp.route('/disponibilidade/<data_inicial>', methods=['GET'])
def get_disponibilidade(data_inicial):
    ocupados = agendamento_service.check_availability(data_inicial)
    return jsonify({
        'data_inicial': data_inicial,
        'agendamentos_ocupados': ocupados
    }), 200

@agendamento_bp.route('/agendar', methods=['POST'])
@jwt_required()
def create_agendamento():
    current_user_email = get_jwt_identity()
    data = request.json
    horario = data.get('horario')
    duracao = data.get('duracao', 30)

    if not horario:
        return jsonify({'erro': 'Horário é obrigatório.'}), 400
    
    try:
        duracao = int(duracao)
    except (ValueError, TypeError):
        return jsonify({'erro': 'Duração deve ser um número inteiro (em minutos).'}), 400
    
    # Busca dados do usuário
    from app.database.repository import get_user_by_email
    user = get_user_by_email(current_user_email)
    
    if not user:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
        
    sucesso, mensagem = agendamento_service.process_new_agendamento(
        user['nome'], 
        user['email'], 
        horario, 
        duracao
    )
    
    if sucesso:
        return jsonify({'mensagem': mensagem, 'horario': horario, 'duracao': duracao}), 201
    else:
        return jsonify({'erro': mensagem}), 409

@agendamento_bp.route('/agendamentos', methods=['GET'])
@jwt_required()
def get_all_agendamentos():
    current_user_email = get_jwt_identity()
    from app.database import repository
    agendamentos = repository.get_agendamentos_by_email(current_user_email)
    return jsonify({
        'total': len(agendamentos),
        'agendamentos': agendamentos
    }), 200