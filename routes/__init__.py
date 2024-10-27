from .blog.blog_routes import init_blog_routes
from .auth.auth_routes import init_auth_routes
from .categories.category_routes import init_category_routes
from .users.users import init_users_routes
from .posts.posts import init_posts_routes

def init_routes(app):
    init_blog_routes(app)
    init_auth_routes(app)
    init_category_routes(app)
    init_users_routes(app)
    init_posts_routes(app)  
