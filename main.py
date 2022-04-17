from flask import Flask, render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from flask_session import Session
import sqlite3

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

@app.route("/")
def index():
  conn = sqlite3.connect('db.sqlite3')
  conn.row_factory=sqlite3.Row
  # Pegar os posts
  cursor=conn.cursor()
  cursor.execute("select * from BLOG_POSTS ORDER BY id DESC")
  post = cursor.fetchall()

  # Pegar o autor
  cursor2=conn.cursor()
  cursor2.execute('SELECT * FROM auth_user WHERE id=? ', (1,))
  autor = cursor2.fetchone()
  
  return render_template("blog/index.html", posts= post, autor=autor)


@app.route('/ver_post/<string:slug>', methods=["POST", "GET"])
def ver_post(slug):
  if request.method == 'POST':
    slug = slug
  conn = sqlite3.connect('db.sqlite3')
  conn.row_factory=sqlite3.Row
  cursor = conn.cursor()
  cursor.execute("select * from BLOG_POSTS where slug=?", (slug,))
  data = cursor.fetchone()
  cursor2=conn.cursor()
  cursor2.execute("select * from auth_user where id=?", (data['author_id'],))
  autor = cursor2.fetchone()
  return render_template('blog/show_post.html', post=data, autor = autor)


@app.route('/categorias')
def pagina_categorias():
  conn = sqlite3.connect('db.sqlite3')
  conn.row_factory=sqlite3.Row
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM blog_categoria')
  categorias = cursor.fetchall()
  return render_template('blog/categorias.html', categorias = categorias)

@app.route('/admin')
def pagina_admin():
  if not session.get('email'):
    flash('Você não está logado.', 'warning')
    return redirect(url_for('pagina_login'))
  return render_template('pagina_admin.html')

@app.route('/login')
def pagina_login():
  return render_template('pagina_login.html')
  
@app.route('/auth_user', methods=['POST', 'GET'])
def auth_user():
  if request.method == "POST":
    email= request.form['email']
    session['email'] = email
    senha= request.form['senha']
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor2=conn.cursor()
    try:
      cursor.execute("select * from auth_user where email=?", (email,))
      cursor2.execute("select * from auth_user where password=?", (senha,))
      user_email = cursor.fetchone()
      user_senha = cursor2.fetchone()
      if email == user_email['email']:
        if senha == user_senha['password']:
          flash(f"Bem vindo(a), {user_email['username']}", "success")
          nome = user_email['username']
          session['nome'] = nome
          return redirect(url_for("index"))
      else:
        flash('Usuário ou senha inválidos.', "danger")
        return redirect(url_for("pagina_login"))
    except:
      flash(f'Nenhum usuário com o email {email}', 'warning')
      return redirect(url_for("pagina_login"))

@app.route("/logout")
def logout():
  session['email'] = None
  return redirect(url_for("index"))

if __name__ == '__main__':
  app.secret_key="admin123"
  app.run(debug=True, port=8080)