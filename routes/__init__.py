from .blog_routes import init_blog_routes
from .auth_routes import init_auth_routes
from .category_routes import init_category_routes

def init_routes(app):
    init_blog_routes(app)
    init_auth_routes(app)
    init_category_routes(app)
