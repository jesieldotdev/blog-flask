from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

Post = [
    {'title': f'Post {i}',
    'slug': f'post-{i}',
    'author': f'author {i}',
    'body': '''Python é uma linguagem de programação de alto nível,[6] interpretada de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte. Foi lançada por Guido van Rossum em 1991.[1] Atualmente, possui um modelo de desenvolvimento comunitário, aberto e gerenciado pela organização sem fins lucrativos Python Software Foundation. Apesar de várias partes da linguagem possuírem padrões e especificações formais, a linguagem, como um todo, não é formalmente especificada. O padrão de facto é a implementação CPython. linguagem foi projetada com a filosofia de enfatizar a importância do esforço do programador sobre o esforço computacional. Prioriza a legibilidade do código sobre a velocidade ou expressividade. Combina uma sintaxe concisa e clara com os recursos poderosos de sua biblioteca padrão e dulos e frameworks desenvolvi por terceiros.''', 'created_at' : f'0{i}:{i}0',
    'updated': 'dia tal',
    'image': 'https://images.unsplash.com/photo-1556075798-4825dfaaf498?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop',
      'categoria': 'GitHub',
      'fontes': 'Desconhecida'} for i in range(5)]
      


@app.route("/")
def index(Post=Post):
  return render_template("index.html", Post=Post)