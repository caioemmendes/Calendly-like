# app/database/repository.py

from app.__init__ import db
from sqlalchemy import text # <-- NOVA IMPORTAÇÃO NECESSÁRIA

# Tabela: Agendamentos (id, nome, email, horario, duracao)
def create_agendamentos_table():
    try:
        # AQUI ESTÁ A CORREÇÃO: Envolver a string SQL com text()
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
        # Erro de conexão ou sintaxe SQL aparecerá aqui
        print(f"Erro CRÍTICO ao criar tabela: {e}")
        db.session.rollback() 
        return False

# ... o restante do seu código ...
# OBS: Você deve aplicar o mesmo text() em todas as suas queries SQL brutas (SELECT, INSERT)
# Exemplo de INSERT corrigido:
def save_new_agendamento(data):
    sql = text("INSERT INTO agendamentos (nome, email, horario, duracao) VALUES (:nome, :email, :horario, :duracao)")
    db.session.execute(sql, data)
    db.session.commit()
    return True

def get_all_agendamentos_in_period(start_date, end_date):
    # Retorna os horários já ocupados
    sql = text("SELECT horario, duracao FROM agendamentos WHERE horario BETWEEN :start AND :end")
    result = db.session.execute(sql, {'start': start_date, 'end': end_date}).fetchall()
    return [dict(row._mapping) for row in result] # Transforma em lista de dicionários

def get_all_agendamentos():
    """Retorna todos os agendamentos cadastrados"""
    sql = text("SELECT id, nome, email, horario, duracao FROM agendamentos ORDER BY horario")
    result = db.session.execute(sql).fetchall()
    return [dict(row._mapping) for row in result]