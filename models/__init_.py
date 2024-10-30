from db import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'))
    author = relationship("AuthUser", backref="posts")
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    
    def create_new_user(self, username, email, password, isAdmin):
      self.username = username
      self.email = email
      self.password = password
      self.isAdmin = isAdmin
      return self
    
    def set_password(self, password):
      self.password = generate_password_hash(password)
      
    def check_user(self, password):
      return check_password_hash(self.password, password)
    

class BlogCategories(db.Model):
    __tablename__ = 'blog_categories'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
