import requests
from flask import render_template, request, flash, redirect, url_for, session

def init_blog_routes(app):
    API_BASE_URL = "https://posts-api-next.vercel.app/api/posts"  # Substitua pela URL base da sua API

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")

    @app.route("/")
    def index():
        try:
            response = requests.get(f"{API_BASE_URL}/")
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            posts = response.json()["posts"]  # Assumindo que a API retorna um JSON
            print(posts)
        except requests.RequestException as e:
            flash("Erro ao buscar posts da API.", "danger")
            posts = []

        isAdmin = session.get("is_admin", False)  # Ajuste baseado na sua lógica de autenticação

        if not posts:
            flash("Nenhuma postagem encontrada.", "info")

        return render_template("blog/home.html", posts=posts, isAdmin=isAdmin)

    @app.route("/post/<string:slug>", methods=["POST", "GET"])
    def see_post(slug):
        try:
            response = requests.get(f"{API_BASE_URL}/posts/{slug}")
            response.raise_for_status()
            post = response.json()["post"]
        except requests.RequestException:
            flash("Postagem não encontrada.", "warning")
            return redirect(url_for("index"))

        try:
            author_id = post.get("author_id")
            author_response = requests.get(f"{API_BASE_URL}/users/{author_id}")
            author_response.raise_for_status()
            autor = author_response.json()["user"]
        except requests.RequestException:
            autor = {"name": "Desconhecido"}

        return render_template("blog/show_post.html", post=post, autor=autor)

    @app.route("/page/<int:post_num>")
    def page(post_num):
        offset = (post_num - 1) * 4
        try:
            response = requests.get(f"{API_BASE_URL}/posts?limit=4&offset={offset}&order=desc")
            response.raise_for_status()
            posts = response.json()["posts"]
        except requests.RequestException:
            flash("Erro ao buscar posts da API.", "danger")
            posts = []

        if not posts:
            flash("Nenhuma postagem encontrada nesta página.", "info")

        return render_template("blog/home.html", posts=posts)
