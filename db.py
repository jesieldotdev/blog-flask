from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Cria a instância do SQLAlchemy

def init_db(app):
    db.init_app(app)  # Inicializa o SQLAlchemy com a instância do Flask
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos modelos
