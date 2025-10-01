from flask import Blueprint, jsonify, request
from app.services import agendamento_service

agendamento_bp = Blueprint('agendamentos', __name__)

@agendamento_bp.route('/disponibilidade/<data_inicial>', methods=['GET'])
def get_disponibilidade(data_inicial):
    ocupados = agendamento_service.check_availability(data_inicial)
    return jsonify({
        'data_inicial': data_inicial,
        'agendamentos_ocupados': ocupados
    }), 200

@agendamento_bp.route('/agendar', methods=['POST'])
def create_agendamento():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    horario = data.get('horario')
    duracao = data.get('duracao', 30)

    if not all([nome, email, horario]):
        return jsonify({'erro': 'Nome, email e horário são obrigatórios.'}), 400
    
    try:
        duracao = int(duracao)
    except (ValueError, TypeError):
        return jsonify({'erro': 'Duração deve ser um número inteiro (em minutos).'}), 400
        
    sucesso, mensagem = agendamento_service.process_new_agendamento(nome, email, horario, duracao)
    
    if sucesso:
        return jsonify({'mensagem': mensagem, 'horario': horario, 'duracao': duracao}), 201
    else:
        return jsonify({'erro': mensagem}), 409

@agendamento_bp.route('/agendamentos', methods=['GET'])
def get_all_agendamentos():
    from app.database import repository
    agendamentos = repository.get_all_agendamentos()
    return jsonify({
        'total': len(agendamentos),
        'agendamentos': agendamentos
    }), 200