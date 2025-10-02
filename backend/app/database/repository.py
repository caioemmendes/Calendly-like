from app.__init__ import db
from sqlalchemy import text

def create_agendamentos_table():
    try:
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                horario DATETIME NOT NULL UNIQUE,
                duracao INT NOT NULL 
            )
        """))
        db.session.commit()
        print("Tabela 'agendamentos' verificada/criada com sucesso.")
        return True
    except Exception as e:
        print(f"Erro CRÍTICO ao criar tabela: {e}")
        db.session.rollback() 
        return False

def create_users_table():
    try:
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        db.session.commit()
        print("Tabela 'usuarios' verificada/criada com sucesso.")
        return True
    except Exception as e:
        print(f"Erro ao criar tabela usuarios: {e}")
        db.session.rollback()
        return False

def create_user(data):
    sql = text("INSERT INTO usuarios (nome, email, senha_hash) VALUES (:nome, :email, :senha_hash)")
    result = db.session.execute(sql, data)
    db.session.commit()
    return result.lastrowid

def get_user_by_email(email):
    sql = text("SELECT id, nome, email, senha_hash FROM usuarios WHERE email = :email")
    result = db.session.execute(sql, {'email': email}).fetchone()
    if result:
        return dict(result._mapping)
    return None

def save_new_agendamento(data):
    sql = text("INSERT INTO agendamentos (nome, email, horario, duracao) VALUES (:nome, :email, :horario, :duracao)")
    db.session.execute(sql, data)
    db.session.commit()
    return True

def get_all_agendamentos_in_period(start_date, end_date):
    sql = text("SELECT horario, duracao FROM agendamentos WHERE horario BETWEEN :start AND :end")
    result = db.session.execute(sql, {'start': start_date, 'end': end_date}).fetchall()
    return [dict(row._mapping) for row in result]

def get_all_agendamentos():
    sql = text("SELECT id, nome, email, horario, duracao FROM agendamentos ORDER BY horario")
    result = db.session.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]

def get_agendamentos_by_email(email):
    sql = text("SELECT id, nome, email, horario, duracao FROM agendamentos WHERE email = :email ORDER BY horario")
    result = db.session.execute(sql, {'email': email}).fetchall()
    return [dict(row._mapping) for row in result]