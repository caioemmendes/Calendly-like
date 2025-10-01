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