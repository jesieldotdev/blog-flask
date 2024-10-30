from flask import render_template, request, flash, redirect, url_for, session
from db import db
from models.__init_ import BlogPost, AuthUser, BlogCategories  # Certifique-se de que seus modelos estão definidos em um arquivo models.py


def init_blog_routes(app):
    @app.errorhandler(404)
    def page_not_found(e):
      return render_template("404.html")
    @app.route("/")
    def index():
        posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(4).all()
        isAdmin = AuthUser.check_if_user_admin(session.get('email'))
         # Supondo que você tenha um usuário com ID 1

        # Tratamento de erro para posts vazios
        if not posts:
            flash('Nenhuma postagem encontrada.', 'info')
        
        return render_template("blog/home.html", posts=posts, isAdmin=isAdmin)

    @app.route('/post/<string:slug>', methods=["POST", "GET"])
    def see_post(slug):
        post = BlogPost.query.filter_by(slug=slug).first()

        # Verifica se o post foi encontrado
        if post is None:
            flash('Postagem não encontrada.', 'warning')
            return redirect(url_for('index'))

        autor = AuthUser.query.get(post.author_id)  # Obtendo o autor pelo author_id
        return render_template('blog/show_post.html', post=post)
 
    @app.route("/page/<int:post_num>")
    def page(post_num):
        offset = (post_num - 1) * 4
        posts = BlogPost.query.order_by(BlogPost.id.desc()).offset(offset).limit(4).all()
        autor = AuthUser.query.get(1)  # Supondo que você tenha um usuário com ID 1

        # Tratamento de erro para posts vazios
        if not posts:
            flash('Nenhuma postagem encontrada nesta página.', 'info')

        return render_template("blog/home.html", posts=posts, autor=autor)
