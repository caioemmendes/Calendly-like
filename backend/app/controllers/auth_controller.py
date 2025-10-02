from flask import Blueprint, jsonify, request
from app.__init__ import db, bcrypt
from app.database.repository import create_user, get_user_by_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, email, senha]):
        return jsonify({'erro': 'Nome, email e senha são obrigatórios'}), 400

    if len(senha) < 6:
        return jsonify({'erro': 'Senha deve ter no mínimo 6 caracteres'}), 400

    # Verifica se usuário já existe
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'erro': 'Email já cadastrado'}), 409

    # Hash da senha
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8')

    # Cria usuário
    try:
        user_id = create_user({
            'nome': nome,
            'email': email,
            'senha_hash': senha_hash
        })

        # Gera token JWT
        access_token = create_access_token(identity=email)

        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso',
            'token': access_token,
            'usuario': {
                'id': user_id,
                'nome': nome,
                'email': email
            }
        }), 201
    except Exception as e:
        return jsonify({'erro': f'Erro ao cadastrar usuário: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not all([email, senha]):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    # Busca usuário
    user = get_user_by_email(email)
    
    if not user:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401

    # Verifica senha
    if not bcrypt.check_password_hash(user['senha_hash'], senha):
        return jsonify({'erro': 'Email ou senha inválidos'}), 401

    # Gera token JWT
    access_token = create_access_token(identity=email)

    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'token': access_token,
        'usuario': {
            'id': user['id'],
            'nome': user['nome'],
            'email': user['email']
        }
    }), 200


@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    current_user_email = get_jwt_identity()
    user = get_user_by_email(current_user_email)
    
    if not user:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    return jsonify({
        'id': user['id'],
        'nome': user['nome'],
        'email': user['email']
    }), 200