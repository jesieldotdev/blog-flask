from flask import render_template, request, redirect, url_for, flash, session
from db import db
from models.__init_ import AuthUser, BlogPost  # Certifique-se de que seus modelos estão definidos em um arquivo models.py

def init_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            remember = bool(request.form.get('remember'))
            user = AuthUser.query.filter_by(email=email).first()
            
            if user and user.password == password:  # Verifique se a senha é a correta
                session['email'] = email
                flash(f"Bem-vindo(a), {user.username}", "success")
                if remember:
                    session['username'] = user.username
                return redirect(url_for("index"))
            flash('Usuário ou senha inválidos.', "danger")
        return render_template("admin/login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    @app.route('/admin')
    def admin():
        if not session.get('email'):
            flash('Você não está logado.', 'warning')
            return redirect(url_for('login'))
        elif(not AuthUser.check_if_user_admin(session["email"])):
          flash("Você não está autorizado.", "danger")
          return redirect(url_for("index"))
        return render_template('admin/admin.html')



    @app.route('/admin/atualizar_e_adicionar_outro/<int:post_id>', methods=["POST"])
    def update_and_add_another(post_id):
      if(not AuthUser.check_if_user_admin(session["email"])):
        flash("Você não está autorizado.", "danger")
        return redirect(url_for("index"))
        # Aqui você pode implementar a lógica para adicionar outro post.
        # Para o exemplo, vamos só redirecionar de volta para a edição do mesmo.
        flash('Postagem atualizada com sucesso! Você pode adicionar outro post agora.', 'success')
        return redirect(url_for('edit_post', post_id=post_id))
