from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''Creates new users'''
    
    __tablename__ = "users"
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    @classmethod
    def register(cls, name, pwd, email, first, last):
        '''Registers a user with an ecrypted password'''
        
        hashed = bcrypt.generate_password_hash(pwd)
        
        password = hashed.decode("utf8")
        
        return cls(
            username=name, password=password, email=email,
            first_name=first, last_name=last
        )
    
    @classmethod
    def authenticate(cls, name, pwd):
        '''Authenticates a user by comparing encrypted passwords'''
        
        user = cls.query.filter_by(username=name).first()
        
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user 
        else:
            return False