from datetime import datetime, date
from verwaltungonline import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique =True, nullable=False)
    email = db.Column(db.String(120), unique =True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)
    post = db.relationship('Post', backref='author', lazy=True)
    
    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
 
    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"

class Einheiten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()


class Gemeinschaft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()

class Kostenarten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Stockwerke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Umlageschluessel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    tabelle1 = db.Column(db.String(25), nullable=False)
    wert1 = db.Column(db.String(25), nullable=False)
    tabelle2 = db.Column(db.String(25), nullable=False)
    wert2 = db.Column(db.String(25), nullable=False)
    operation = db.Column(db.String(1), nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Vermietung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weid = db.Column(db.String(5), unique=True, nullable=False)
    wohnung = db.Column(db.String(4), nullable=False)
    #wohnung = db.Column(db.Integer, db.ForeignKey('wohnungen.nummer'),nullable=False)
    vorname = db.Column(db.String(20), nullable=False)
    nachname = db.Column(db.String(20), nullable=False)
    strasse = db.Column(db.String(30), nullable=False)
    hausnummer = db.Column(db.String(10), nullable=False)
    plz = db.Column(db.String(5), nullable=False)
    ort = db.Column(db.String(30), nullable=False)
    mietbeginn = db.Column(db.Date, nullable=False)
    mietende = db.Column(db.Date, nullable=True)
    personen = db.Column(db.String(2), nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Wohnungen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(4), unique=True, nullable=False)
    stockwerk = db.Column(db.String(25), unique=False, nullable=False)
    #stockwerk = db.Column(db.Integer, db.ForeignKey('stockwerke.bezeichnung'),nullable=False)
    qm = db.Column(db.String(10), nullable=False)
    zimmer = db.Column(db.String(2), nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()

class Zaehler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(50), nullable=False)
    typ = db.Column(db.String(25), nullable=False)
    #typ = db.Column(db.Integer, db.ForeignKey('zaehlertypen.bezeichnung'),nullable=False)
    gemeinschaft = db.Column(db.Boolean(), nullable=False)
    wohnung = db.Column(db.String(4), nullable=False)
    #wohnung = db.Column(db.Integer, db.ForeignKey('wohnungen.nummer'),nullable=False)
    ort = db.Column(db.String(30), nullable=False)
        
    def __repr__(self) -> str:
        return super().__repr__()

class Zaehlertypen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return super().__repr__()


with app.app_context():
    db.create_all()