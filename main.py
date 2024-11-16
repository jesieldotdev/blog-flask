from flask import Flask
from flask_authz import CasbinEnforcer
from db import db, init_db  # Certifique-se de importar db e init_db
from models.__init_ import AuthUser
from routes import init_routes
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

# Configurações do aplicativo
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
# Configuração para o Supabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres.smjvdyhhwzdzvloweoxt:SnarkyPump77@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CASBIN_MODEL'] = 'model.conf'
app.config['CASBIN_POLICY'] = 'policy.csv'

# Inicializar o enforcer do Casbin
enforcer = CasbinEnforcer(app)

# Inicializar banco de dados
init_db(app)

# Verifica se existem usuários no banco
# with app.app_context():
#     if not AuthUser.query.first():
#         user = AuthUser(email='jesiel364@gmail.com',
#                         username="jesiel", isAdmin=True, password="1245")
#         db.session.add(user)
#         db.session.commit()

# Inicializa as rotas
init_routes(app)

if __name__ == '__main__':
    app.secret_key = "1245"
    app.run(debug=True, port=8080)
