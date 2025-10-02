from app.__init__ import create_app
from app.database.repository import create_agendamentos_table, create_users_table
from dotenv import load_dotenv

load_dotenv()
app = create_app()

with app.app_context():
    create_agendamentos_table()
    create_users_table()

if __name__ == '__main__':
    app.run(debug=True)