from flask import Blueprint, jsonify, request
from flask_mail import Message
from app.services import agendamento_service
from app.utils.email_sender import send_confirmation_email # Função simples a ser criada
from app.__init__ import mail # Importa a instância do Flask-Mail
from app.database import repository  # Importe o repository

agendamento_bp = Blueprint('agendamentos', __name__)

# Rota de Disponibilidade
@agendamento_bp.route('/api/v1/disponibilidade/<data_inicial>', methods=['GET'])
def get_disponibilidade(data_inicial):
    # data_inicial deve ser YYYY-MM-DD
    disponiveis = agendamento_service.check_availability(data_inicial)
    return jsonify({
        'data_inicial': data_inicial,
        'horarios': disponiveis
    }), 200

# Rota de Agendamento
@agendamento_bp.route('/api/v1/agendar', methods=['POST'])
def create_agendamento():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    horario = data.get('horario') 

    if not all([nome, email, horario]):
        return jsonify({'erro': 'Nome, email e horário são obrigatórios.'}), 400
        
    sucesso, mensagem = agendamento_service.process_new_agendamento(nome, email, horario)
    
    if sucesso:
        # --- CHAMADA DO SERVICE DE E-MAIL ---
        send_confirmation_email(email, nome, horario)
        
        return jsonify({'mensagem': mensagem, 'horario': horario}), 201
    else:
        return jsonify({'erro': mensagem}), 409
    
    # Nova rota GET para listar todos os agendamentos
@agendamento_bp.route('/api/v1/agendamentos', methods=['GET'])
def get_all_agendamentos():
    agendamentos = repository.get_all_agendamentos()
    return jsonify({
        'total': len(agendamentos),
        'agendamentos': agendamentos
    }), 200