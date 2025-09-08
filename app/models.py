from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    # 'manager' or 'employee'
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"
