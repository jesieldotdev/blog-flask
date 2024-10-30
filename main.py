from flask import Flask
from flask_authz import CasbinEnforcer
from db import db, init_db  # Certifique-se de importar db e init_db
from models.__init_ import AuthUser
from routes import init_routes

app = Flask(__name__)

# Configurações do aplicativo
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
# Modo de leitura e escrita
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db?mode=rw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CASBIN_MODEL'] = 'model.conf'
app.config['CASBIN_POLICY'] = 'policy.csv'
enforcer = CasbinEnforcer(app)
# Inicializar banco de dados
init_db(app)
with app.app_context():
    if not AuthUser.query.first():  # Verifica se já existem usuários
        user = AuthUser(email='jesiel364@gmail.com',
                        username="jesiel", isAdmin=True, password="1245")
        db.session.add(user)
        db.session.commit()  # Passa o app para a função que inicializa o banco de dados
init_routes(app)

if __name__ == '__main__':
    app.secret_key = "1245"
    app.run(debug=True, port=8080)
