from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)  # Inicializa a instância do SQLAlchemy com o app
    with app.app_context():  # Garante que você está no contexto do app
        db.create_all()  # Cria todas as tabelas definidas nos modelos
    
