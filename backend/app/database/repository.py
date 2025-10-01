# app/database/repository.py

from app.__init__ import db

# Tabela: Agendamentos (id, nome, email, horario, duracao)
def create_agendamentos_table(): # <-- O NOME DA FUNÇÃO DEVE SER EXATAMENTE ESTE
    # Isso seria rodado uma vez na inicialização ou migração.
    try:
        # Note que a sintaxe SQL aqui deve ser correta para o seu MySQL
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                horario DATETIME NOT NULL UNIQUE,
                duracao INT NOT NULL 
            )
        """)
        db.session.commit()
        return True # Retorna algo para indicar sucesso (opcional)
    except Exception as e:
        # Se houver erro de conexão com o MySQL, ele aparecerá aqui
        print(f"Erro ao criar tabela: {e}")
        db.session.rollback() # Garante que o estado do DB seja limpo
        return False

# ... O restante das funções do Repository (get_all_agendamentos_in_period, save_new_agendamento, etc.)