from flask import Flask
from flask_session import Session
from db import db, init_db  # Importando a instância do db e a função init_db
from routes import init_routes  # Importando a função que inicializa as rotas

app = Flask(__name__)

# Configurações de sessão
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a sessão
Session(app)

# Inicializa o banco de dados
init_db(app)

# Inicializa as rotas
init_routes(app)

if __name__ == '__main__':
    app.secret_key = "1245"  # Chave secreta para sessões
    app.run(debug=True, port=8080)  # Executa a aplicação em modo de depuração na porta 8080
