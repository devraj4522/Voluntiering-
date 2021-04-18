from werkzeug.security import generate_password_hash, check_password_hash
from app_config import crete_datebase, app
from flask_login import UserMixin

# MySql Database 
db = crete_datebase(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(280), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    roles = db.relationship('Role', secondary='user_role')

    def __init__(self, username, address, password, email):
        self.username = username
        self.address = address
        self.email = email
        self.password = generate_password_hash(password, salt_length=10)

    
    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Voluntier(db.Model, UserMixin):
    __tablename__ = "voluntier"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mob = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    gov_doc = db.Column(db.String(100), nullable=False)
    quallifacations = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    
    def __init__(self, name, email, mob, state, district, bio, gov_doc, quallifacations, password):
        self.name = name
        self.email = email
        self.mob = mob
        self.state = state
        self.district = district
        self.bio = bio
        self.gov_doc = gov_doc
        self.quallifacations = quallifacations
        self.password = generate_password_hash(password, salt_length=10)

    
    def __repr__(self):
        return '<Voluntier %r>' % self.name

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(520), nullable=False)

    voluntier_id = db.Column(db.Integer, db.ForeignKey('voluntier.id'),
        nullable=False)
    voluntier = db.relationship('Voluntier',
        backref=db.backref('messages', lazy=True))

    def __init__(self, msg, voluntier):
        self.msg = msg
        self.voluntier = voluntier

    def __repr__(self):
        return '<Message %r>' % self.id

# db.create_all()

# new_role = Role(name='Voluntier')
# db.session.add(new_role)
# db.session.commit()