from flask import render_template, request, redirect, url_for, flash, session
from db import db
from models.__init_ import AuthUser, BlogPost
from utils.utils import admin_required

def init_users_routes(app):
    @app.route('/admin/users_list', methods=["GET"])
    @admin_required
    def users_list():
        users = AuthUser.query.order_by(AuthUser.id.desc()).all()
        return render_template('admin/user/user_list.html', users=users)

    @app.route("/admin/create_user", methods=["GET", "POST"])
    @admin_required
    def create_user():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            isAdmin = request.form['isAdmin'] == 'true'

            new_user = AuthUser.create_new_user(username, email, password, isAdmin)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('users_list'))

        return render_template('admin/user/create_user.html')

    @app.route('/admin/edit_user/<int:user_id>', methods=["GET"])
    @admin_required
    def edit_user(user_id):
        user = AuthUser.query.get(user_id)
        if user is None:
            flash('Usuário não encontrado.', 'warning')
            return redirect(url_for('users_list'))
        return render_template('admin/user/edit_user.html', user=user)

    @app.route('/admin/update_user/<int:user_id>', methods=["POST"])
    @admin_required
    def update_user(user_id):
        user = AuthUser.query.get(user_id)
        if user is None:
            flash('Usuário não encontrado.', 'warning')
            return redirect(url_for('users_list'))

        user.username = request.form.get('username')
        user.email = request.form.get('email')
        if request.form.get('password') != '':
            user.password = request.form.get('password')
        user.isAdmin = request.form.get('isAdmin') == 'true'

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('users_list'))

    @app.route('/admin/delete_user/<int:user_id>', methods=["GET"])
    @admin_required
    def delete_user(user_id):
        AuthUser.query.filter(AuthUser.id == user_id).delete()
        db.session.commit()
        flash('Usuário removido.', 'warning')
        return redirect(url_for('users_list'))