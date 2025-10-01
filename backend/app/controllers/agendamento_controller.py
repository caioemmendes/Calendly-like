from flask import Blueprint, jsonify, request
from app.services import agendamento_service

agendamento_bp = Blueprint('agendamentos', __name__)

# Rota de Disponibilidade
@agendamento_bp.route('/api/v1/disponibilidade/<data_inicial>', methods=['GET'])
def get_disponibilidade(data_inicial):
    disponiveis = agendamento_service.check_availability(data_inicial)
    return jsonify({
        'data_inicial': data_inicial,
        'horarios': disponiveis
    }), 200

# Rota de Agendamento
@agendamento_bp.route('/agendar', methods=['POST'])
def create_agendamento():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    horario = data.get('horario') 
    duracao = data.get('duracao')

    if not all([nome, email, horario, duracao]):
        return jsonify({'erro': 'Nome, email, horário e duração são obrigatórios.'}), 400
        
    sucesso, mensagem = agendamento_service.process_new_agendamento(nome, email, horario, duracao)
    
    if sucesso:
        return jsonify({'mensagem': mensagem, 'horario': horario}), 201
    else:
        return jsonify({'erro': mensagem}), 409

# Rota para listar todos os agendamentos
@agendamento_bp.route('/allagendamentos', methods=['GET'])
def get_all_agendamentos():
    from app.database import repository
    agendamentos = repository.get_all_agendamentos()
    return jsonify({
        'total': len(agendamentos),
        'agendamentos': agendamentos
    }), 200