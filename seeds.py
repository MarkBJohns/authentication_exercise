from models import db, User
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()
    
    u1 = User.register(
        name="JohnDoe47", pwd="Password123", email="john.doe.47@company.com",
        first="John", last="Doe"
    )
    
    db.session.add_all([u1])
    db.session.commit()
    