from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import sqlite3

app = Flask(__name__)

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
  return render_template('pagina_admin.html')

@app.route('/login')
def pagina_login():
  return render_template('pagina_login.html')
  
@app.route('/auth_user', methods=['POST', 'GET'])
def auth_user():
  if request.method == "POST":
    email= request.form['email']
    senha= request.form['senha']
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("select * from auth_user where email=?", (email,))
    autor = cursor.fetchone()
    
  return (f"Bem vindo, {autor['username']}")
   

if __name__ == '__main__':
  app.run(debug=True, port=8080)