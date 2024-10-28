from flask import render_template, request, redirect, url_for, flash, session
from db import db
# Certifique-se de que seus modelos estão definidos em um arquivo models.py
from models.__init_ import  BlogPost, AuthUser


def init_posts_routes(app):
    @app.route("/admin/create_post", methods=["GET", "POST"])
    def create_post():
        users = AuthUser.query.order_by(AuthUser.id.desc()).all()
        if request.method == 'POST':
            title = request.form['title']
            slug = request.form['slug']
            body = request.form['body']
            # Supondo que você tenha um campo para o ID do autor
            author_id = request.form['author_id']
            image = request.form['image']

            new_post = BlogPost(title=title, slug=slug,
                                body=body, author_id=author_id, image=image)
            db.session.add(new_post)
            db.session.commit()
            flash('Postagem criada com sucesso!', 'success')
            return redirect(url_for('post_list'))

        return render_template('admin/post/create_post.html', users=users)
    
    
    

    @app.route('/admin/edit_post/<int:post_id>', methods=["GET"])
    
    def edit_post(post_id):
        users = AuthUser.query.order_by(AuthUser.id.desc()).all()
        post = BlogPost.query.get(post_id)
        if post is None:
            flash('Postagem não encontrada.', 'warning')
            return redirect(url_for('post_list'))
        return render_template('admin/post/edit_post.html', post=post, users=users)
    
    
    

    @app.route('/admin/update_post/<int:post_id>', methods=["POST"])
    def update_post(post_id):
        post = BlogPost.query.get(post_id)
        if post is None:
            flash('Postagem não encontrada.', 'warning')
            return redirect(url_for('post_list'))

        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.body = request.form.get('body')
        # Assumindo que o autor seja fornecido no formulário
        post.author_id = request.form.get('author_id')
        post.image = request.form.get('image')

        db.session.commit()
        flash('Postagem atualizada com sucesso!', 'success')
        return redirect(url_for('post_list'))
    
    
    

    @app.route('/admin/descartar/<int:post_id>', methods=["GET"])
    def discard_changes(post_id):
        BlogPost.query.filter(BlogPost.id == post_id).delete()
        db.session.commit()
        flash('Alterações descartadas.', 'info')
        return redirect(url_for('post_list'))
    
    
    

    @app.route('/admin/post_list', methods=["GET"])
    def post_list():
        posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
        return render_template('admin/post/post_list.html', posts=posts)
