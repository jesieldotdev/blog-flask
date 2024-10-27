from db import db


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
class BlogCategories(db.Model):
    __tablename__ = 'blog_categories'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
