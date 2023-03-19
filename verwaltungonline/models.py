from datetime import datetime

from attr import NOTHING
from verwaltungonline import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Datenbank Model für User"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.jpg")
    password = db.Column(db.String(60), nullable=True)
    post = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"


class Ablesung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weid_id = db.Column(db.Integer, db.ForeignKey("vermietung.id", name='fk_ablesung_vermietung_weid'), index=True)
    datum = db.Column(db.Date, nullable=False)
    abrechnungsjahr = db.Column(db.String(4), nullable=False)
    wohnung_id = db.Column(db.Integer, db.ForeignKey("wohnungen.id", name='fk_ablesung_wohnungen_id'), index=True)
    ort_id = db.Column(db.Integer, db.ForeignKey('zaehler.ort', name='fk_ablesung_zaehler_ort'), nullable=False, index=True)
    zaehler_id = db.Column(db.Integer, db.ForeignKey('zaehler.id', name='fk_ablesung_zaehler_id'), nullable=False, index=True)
    zaehlertyp_id = db.Column(db.Integer, db.ForeignKey('zaehlertypen.id', name='fk_ablesung_zaehlertypen_id'), nullable=False, index=True)
    ablesewert = db.Column(db.Float(precision=2), nullable=False)
    weid = db.relationship('Vermietung', backref='ablesung')
    wohnung = db.relationship('Wohnungen', backref='ablesung')
    zaehler_ort = db.relationship('Zaehler', foreign_keys=[ort_id], backref='ablesung_ort')
    zaehler_id_fk = db.relationship('Zaehler', foreign_keys=[zaehler_id], backref='ablesung_id_fk')
    zaehlertyp = db.relationship('Zaehlertypen', backref='ablesung')


    
    
    # id = db.Column(db.Integer, primary_key=True)
    # weid_id = db.Column(db.Integer, db.ForeignKey("vermietung.id", name='fk_ablesung_vermietung_weid'))
    # datum = db.Column(db.Date, nullable=False)
    # abrechnungsjahr = db.Column(db.String(4), nullable=False)
    # wohnung_id = db.Column(db.Integer, db.ForeignKey("vermietung.wohnung_id", name='fk_ablesung_vermietung_wohnung'))
    # ort_id = db.Column(db.Integer, db.ForeignKey('zaehler.ort', name='fk_ablesung_zaehler_ort'), nullable=False)
    # zaehler_id = db.Column(db.Integer, db.ForeignKey('zaehler.id', name='fk_ablesung_zaehler_id'), nullable=False)
    # zaehlertyp_id = db.Column(db.Integer, db.ForeignKey('zaehlertypen.id', name='fk_ablesung_zaehlertypen_id'), nullable=False)
    # ablesewert = db.Column(db.Float(precision=2), nullable=False)
    # weid = db.relationship('Vermietung', backref='ablesung')
    # wohnung = db.relationship('Vermietung', backref='ablesung')
    # ort = db.relationship('Zaehler', backref='ablesung')
    # zaehler = db.relationship('Zaehler', backref='ablesung')
    # zaehlertyp = db.relationship('Zaehlertypen', backref='ablesung')


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


class Kosten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date, nullable=False)
    abrechnungsjahr = db.Column(db.String(4), nullable=False)
    kostenarten_id = db.Column(db.ForeignKey('kostenarten.id', name='fk_kosten_kostenart_id'), nullable=False)
    firma = db.Column(db.String(30), nullable=False)
    leistung = db.Column(db.String(30), nullable=False)
    betrag = db.Column(db.Float(precision=2), nullable=False)
    menge = db.Column(db.Integer, nullable=False)
    einheiten_id = db.Column(db.ForeignKey('einheiten.id', name='fk_kosten_einheit_id'), nullable=False)
    umlageschluessel_id = db.Column(db.ForeignKey('umlageschluessel.id', name='fk_kosten_umlageschluessel_id'), nullable=False)
    kostenart = db.relationship('Kostenarten', backref='kosten')
    einheit = db.relationship('Einheiten', backref='kosten')
    umlageschluessel = db.relationship('Umlageschluessel', backref='kosten')

    def __repr__(self):
        return super().__repr__()


class Stockwerke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Stockwerke {self.bezeichnung}"


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
    wohnung_id = db.Column(db.Integer, db.ForeignKey('wohnungen.id', name='fk_vermietung_wohnungen_id'), nullable=False)
    vorname = db.Column(db.String(20), nullable=False)
    nachname = db.Column(db.String(20), nullable=False)
    strasse = db.Column(db.String(30), nullable=False)
    hausnummer = db.Column(db.String(10), nullable=False)
    plz = db.Column(db.String(5), nullable=False)
    ort = db.Column(db.String(30), nullable=False)
    mietbeginn = db.Column(db.Date, nullable=False)
    mietende = db.Column(db.Date, nullable=True)
    personen = db.Column(db.String(2), nullable=False)
    wohnung = db.relationship('Wohnungen', backref='vermietung')

    def __repr__(self) -> str:
        return super().__repr__()


class Wohnungen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(4), unique=True, nullable=False)
    stockwerk_id = db.Column(db.Integer, db.ForeignKey('stockwerke.id', name='fk_wohnungen_stockwerke_id'), nullable=False)
    qm = db.Column(db.String(10), nullable=False)
    zimmer = db.Column(db.String(2), nullable=False)
    stockwerk = db.relationship("Stockwerke", backref='wohnungen')

    def __repr__(self) -> str:
        return super().__repr__()


class Zaehler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(50), nullable=False)
    typ_id = db.Column(db.Integer, db.ForeignKey('zaehlertypen.id', name='fk_zaehler_zaehlertypen_id'), nullable=False)
    gemeinschaft = db.Column(db.String(4), nullable=False)
    wohnung_id = db.Column(db.Integer, db.ForeignKey('wohnungen.id', name='fk_zaehler_wohnungen_id'), nullable=False)
    ort = db.Column(db.String(30), nullable=False)
    typ = db.relationship("Zaehlertypen", backref='zaehler')
    wohnung = db.relationship("Wohnungen", backref='zaehler')

    def __repr__(self) -> str:
        return super().__repr__()


class Zaehlertypen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


with app.app_context():
    db.create_all()
