from flask import render_template, request, redirect, url_for, flash, session
from db import db
from models.__init_ import AuthUser, BlogPost  # Certifique-se de que seus modelos estão definidos em um arquivo models.py

def init_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            lembrar = bool(request.form.get('lembrar'))
            user = AuthUser.query.filter_by(email=email).first()
            
            if user and user.password == senha:  # Verifique se a senha é a correta
                session['email'] = email
                flash(f"Bem-vindo(a), {user.username}", "success")
                if lembrar:
                    session['nome'] = user.username
                return redirect(url_for("index"))
            flash('Usuário ou senha inválidos.', "danger")
        return render_template("admin/pagina_login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route('/admin')
    def admin():
        if not session.get('email'):
            flash('Você não está logado.', 'warning')
            return redirect(url_for('login'))
        return render_template('admin/pagina_admin.html')

    @app.route("/admin/criar_post", methods=["GET", "POST"])
    def create_post():
        if request.method == 'POST':
            title = request.form['title']
            slug = request.form['slug']
            body = request.form['body']
            author_id = request.form['author_id']  # Supondo que você tenha um campo para o ID do autor
            image = request.form['image']

            new_post = BlogPost(title=title, slug=slug, body=body, author_id=author_id, image=image)
            db.session.add(new_post)
            db.session.commit()
            flash('Postagem criada com sucesso!', 'success')
            return redirect(url_for('listar_posts'))
        
        return render_template('admin/criar_post.html')

    @app.route('/admin/editar_post/<int:post_id>', methods=["GET"])
    def editar_post(post_id):
        post = BlogPost.query.get(post_id)
        if post is None:
            flash('Postagem não encontrada.', 'warning')
            return redirect(url_for('listar_posts'))
        return render_template('admin/editar_post.html', post=post)

    @app.route('/admin/atualizar_post/<int:post_id>', methods=["POST"])
    def update_post(post_id):
        post = BlogPost.query.get(post_id)
        if post is None:
            flash('Postagem não encontrada.', 'warning')
            return redirect(url_for('listar_posts'))

        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.body = request.form.get('body')
        post.author_id = request.form.get('author')  # Assumindo que o autor seja fornecido no formulário
        post.image = request.form.get('image')

        db.session.commit()
        flash('Postagem atualizada com sucesso!', 'success')
        return redirect(url_for('listar_posts'))

    @app.route('/admin/descartar/<int:post_id>', methods=["GET"])
    def discard_changes(post_id):
        flash('Alterações descartadas.', 'info')
        return redirect(url_for('listar_posts'))

    @app.route('/admin/listar_posts', methods=["GET"])
    def listar_posts():
        posts = BlogPost.query.order_by(BlogPost.id.desc()).all()
        return render_template('admin/listar_posts.html', posts=posts)

    @app.route('/admin/atualizar_e_adicionar_outro/<int:post_id>', methods=["POST"])
    def update_and_add_another(post_id):
        # Aqui você pode implementar a lógica para adicionar outro post.
        # Para o exemplo, vamos só redirecionar de volta para a edição do mesmo.
        flash('Postagem atualizada com sucesso! Você pode adicionar outro post agora.', 'success')
        return redirect(url_for('editar_post', post_id=post_id))
