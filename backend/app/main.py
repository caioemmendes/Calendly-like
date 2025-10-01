# main.py
from app.__init__ import create_app
from app.database.repository import create_agendamentos_table # Importa a função de criação de tabela

app = create_app()

with app.app_context():
    # Cria a tabela ao rodar o app pela primeira vez
    create_agendamentos_table() 

if __name__ == '__main__':
    app.run(debug=True)