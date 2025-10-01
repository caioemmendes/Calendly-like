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