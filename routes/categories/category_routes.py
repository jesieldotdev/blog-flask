from flask import render_template
from db import db
from models.__init_ import BlogCategories  # Certifique-se de que seu modelo está definido em models.py

def init_category_routes(app):
    @app.route('/categorias')
    def pagina_categorias():
        categorias = BlogCategories.query.all()  # Busca todas as categorias
        return render_template('blog/categorias.html', categorias=categorias)
