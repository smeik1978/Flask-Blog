from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    IntegerField,
    DateField,
    SelectField,
    FloatField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from verwaltungonline.models import (
    User,
    Einheiten,
    Gemeinschaft,
    Kosten,
    Kostenarten,
    Stockwerke,
    Umlageschluessel,
    Vermietung,
    Wohnungen,
    Zaehler,
    Zaehlertypen,
)


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class AddEinheit(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        einheit = Einheiten.query.filter_by(bezeichnung=bezeichnung.data).first()
        if einheit:
            raise ValidationError("Diese Einheit gibt es schon!")


class EditEinheit(FlaskForm):
    einheit = SelectField('Einheit', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditEinheit, self).__init__(*args, **kwargs)
        self.einheit.choices = [(e.id, e.bezeichnung) for e in Einheiten.query.all()]

        
class DeleteEinheit(FlaskForm):
    einheit = SelectField('Einheit', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.einheit.choices = [(str(e.id), e.bezeichnung) for e in Einheiten.query.all()]
        

class AddGemeinschaft(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        gemeinschaft = Gemeinschaft.query.filter_by(
            bezeichnung=bezeichnung.data
        ).first()
        if gemeinschaft:
            raise ValidationError("Diese Fläche gibt es schon!")


class EditGemeinschaft(FlaskForm):
    gemeinschaft = SelectField('Gemeinschaft', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditGemeinschaft, self).__init__(*args, **kwargs)
        self.gemeinschaft.choices = [(e.id, e.bezeichnung) for e in Gemeinschaft.query.all()]

        
class DeleteGemeinschaft(FlaskForm):
    gemeinschaft = SelectField('Gemeinschaft', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gemeinschaft.choices = [(str(e.id), e.bezeichnung) for e in Gemeinschaft.query.all()]


class AddKosten(FlaskForm):
    datum = DateField("Datum", validators=[DataRequired()])
    abrechnungsjahr = StringField("Abrechnungsjahr", validators=[DataRequired(), Length(max=4)])
    kostenart = SelectField("Kostenart", choices=[], validators=[DataRequired()])
    firma = StringField("Firma", validators=[DataRequired(), Length(max=30)])
    leistung = StringField("Leistung", validators=[DataRequired(), Length(max=30)])
    betrag = FloatField("Betrag", validators=[DataRequired()])
    menge = IntegerField("Menge", validators=[DataRequired()])
    einheit = SelectField("Einheit", choices=[], validators=[DataRequired()])
    umlageschluessel = SelectField("Umlageschluessel", choices=[], validators=[DataRequired()])
    submit = SubmitField("Speichern")

    def __init__(self, *args, **kwargs):
        super(AddKosten, self).__init__(*args, **kwargs)
        self.kostenart.choices = [(e.id, e.bezeichnung) for e in Kostenarten.query.all()]
        self.einheit.choices = [(e.id, e.bezeichnung) for e in Einheiten.query.all()]
        self.umlageschluessel.choices = [(e.id, e.bezeichnung) for e in Umlageschluessel.query.all()]

    def validate_bezeichnung(self, bezeichnung):
        leistung = Kosten.query.filter_by(
            leistung=leistung.data
        ).first()
        if leistung:
            raise ValidationError("Diese Leistung gibt es schon!")


class EditKosten(FlaskForm):
    datum = DateField("Datum", format='%Y-%m-%d', validators=[DataRequired()])
    abrechnungsjahr = StringField("Abrechnungsjahr", validators=[DataRequired(), Length(max=4)])
    kostenarten = SelectField("Kostenart", choices=[], validators=[DataRequired()])
    firma = StringField("Firma", validators=[DataRequired(), Length(max=30)])
    selleistung = SelectField("Leistung", choices=[])
    leistung = StringField("Neuer Wert für Leistung", validators=[DataRequired(), Length(max=30)])
    betrag = FloatField("Betrag", validators=[DataRequired()])
    menge = IntegerField("Menge", validators=[DataRequired()])
    einheiten = SelectField("Einheit", choices=[], validators=[DataRequired()])
    umlageschluessel = SelectField("Umlageschluessel", choices=[], validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditKosten, self).__init__(*args, **kwargs)
        self.selleistung.choices = [(e.id, e.leistung) for e in Kosten.query.all()]
        self.kostenarten.choices = [(e.id, e.bezeichnung) for e in Kostenarten.query.all()]
        self.einheiten.choices = [(e.id, e.bezeichnung) for e in Einheiten.query.all()]
        self.umlageschluessel.choices = [(e.id, e.bezeichnung) for e in Umlageschluessel.query.all()]


class DeleteKosten(FlaskForm):
    leistung = SelectField('Leistung', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.leistung.choices = [(str(e.id), e.leistung) for e in Kosten.query.all()]


class AddKostenart(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        kostenart = Kostenarten.query.filter_by(bezeichnung=bezeichnung.data).first()
        if kostenart:
            raise ValidationError("Diese Kostenart gibt es schon!")


class EditKostenarten(FlaskForm):
    kostenarten = SelectField('Kostenarten', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditKostenarten, self).__init__(*args, **kwargs)
        self.kostenarten.choices = [(e.id, e.bezeichnung) for e in Kostenarten.query.all()]

        
class DeleteKostenarten(FlaskForm):
    kostenarten = SelectField('Kostenarten', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kostenarten.choices = [(str(e.id), e.bezeichnung) for e in Kostenarten.query.all()]


class AddStockwerk(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        stockwerk = Stockwerke.query.filter_by(bezeichnung=bezeichnung.data).first()
        if stockwerk:
            raise ValidationError("Dieses Stockwerk gibt es schon!")


class EditStockwerke(FlaskForm):
    stockwerke = SelectField('Stockwerke', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditStockwerke, self).__init__(*args, **kwargs)
        self.stockwerke.choices = [(e.id, e.bezeichnung) for e in Stockwerke.query.all()]

        
class DeleteStockwerke(FlaskForm):
    stockwerke = SelectField('Stockwerke', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stockwerke.choices = [(str(e.id), e.bezeichnung) for e in Stockwerke.query.all()]


class AddUmlageschluessel(FlaskForm):
    bezeichnung = StringField("Bezeichnung", validators=[DataRequired(), Length(max=25)])
    tabelle1 = StringField("Tabelle1", validators=[DataRequired(), Length(max=25)])
    wert1 = StringField("Wert1", validators=[DataRequired(), Length(max=25)])
    tabelle2 = StringField("Tabelle2", validators=[DataRequired(), Length(max=25)])
    wert2 = StringField("Wert2", validators=[DataRequired(), Length(max=25)])
    operation = StringField("Operation", validators=[DataRequired(), Length(max=1)])
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        bezeichnung = Umlageschluessel.query.filter_by(
            bezeichnung=bezeichnung.data
        ).first()
        if bezeichnung:
            raise ValidationError("Diesen Schlüssel gibt es schon!")


class EditUmlageschluessel(FlaskForm):
    select_bezeichnung = SelectField('Bezeichnung', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    select_tabelle1 = SelectField('Tabelle1', choices=[], validators=[DataRequired()])
    tabelle1 = StringField('Tabelle1', validators=[DataRequired(), Length(max=25)])
    select_wert1 = SelectField('Wert1', choices=[], validators=[DataRequired()])
    wert1 = StringField('Wert1', validators=[DataRequired(), Length(max=25)])
    select_tabelle2 = SelectField('Tabelle2', choices=[], validators=[DataRequired()])
    tabelle2 = StringField('Tabelle2', validators=[DataRequired(), Length(max=25)])
    select_wert2 = SelectField('Wert2', choices=[], validators=[DataRequired()])
    wert2 = StringField('Wert2', validators=[DataRequired(), Length(max=25)])
    select_operation = SelectField('Operation', choices=[], validators=[DataRequired()])
    operation = StringField('Operation', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditUmlageschluessel, self).__init__(*args, **kwargs)
        self.select_bezeichnung.choices = [(e.id, e.bezeichnung) for e in Umlageschluessel.query.all()]
        self.select_tabelle1.choices = [(e.id, e.tabelle1) for e in Umlageschluessel.query.all()]
        self.select_wert1.choices = [(e.id, e.wert1) for e in Umlageschluessel.query.all()]
        self.select_tabelle2.choices = [(e.id, e.tabelle2) for e in Umlageschluessel.query.all()]
        self.select_wert2.choices = [(e.id, e.wert2) for e in Umlageschluessel.query.all()]
        self.select_operation.choices = [(e.id, e.operation) for e in Umlageschluessel.query.all()]

        
class DeleteUmlageschluessel(FlaskForm):
    umlageschluessel = SelectField('Umlageschluessel', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.umlageschluessel.choices = [(str(e.id), e.bezeichnung) for e in Umlageschluessel.query.all()]


class AddWohnung(FlaskForm):
    nummer = StringField('Wohnung', validators=[DataRequired()])
    stockwerk = SelectField('Stockwerk', choices=[], validators=[DataRequired()])
    qm = StringField('Quadratmeter', validators=[DataRequired()])
    zimmer = StringField('Zimmer', validators=[DataRequired()])
    submit = SubmitField("Speichern")

    def validate_nummer(self, nummer):
        nummer = Wohnungen.query.filter_by(nummer=nummer.data).first()
        if nummer:
            raise ValidationError("Diese Wohnung gibt es schon!")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stockwerk.choices = [(str(e.id), e.bezeichnung) for e in Stockwerke.query.all()]


class EditWohnungen(FlaskForm):
    selnummer = SelectField('Nummer', choices=[], validators=[DataRequired()])
    nummer = StringField('Neue Nummer', validators=[DataRequired()])
    stockwerk = SelectField('Stockwerk', choices=[], validators=[DataRequired()])
    qm = StringField('Quadratmeter', validators=[DataRequired()])
    zimmer = StringField('Zimmer', validators=[DataRequired()])
    submit = SubmitField('Speichern')

    def validate_nummer(self, nummer):
        pass
        # nummer = Wohnungen.query.filter_by(nummer=nummer.data).first()
        # if nummer:
        #     raise ValidationError("Diese Wohnung gibt es schon!")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selnummer.choices = [(e.id, e.nummer) for e in Wohnungen.query.all()]
        self.stockwerk.choices = [(e.id, e.bezeichnung) for e in Stockwerke.query.all()]

        
class DeleteWohnungen(FlaskForm):
    nummer = SelectField('Nummer', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nummer.choices = [(str(e.id), e.nummer) for e in Wohnungen.query.all()]


class AddZaehler(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        zaehler = Zaehler.query.filter_by(bezeichnung=bezeichnung.data).first()
        if zaehler:
            raise ValidationError("Diesen Zähler gibt es schon!")


class EditZaehler(FlaskForm):
    zaehler = SelectField('Zaehler', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditZaehler, self).__init__(*args, **kwargs)
        self.zaehler.choices = [(e.id, e.bezeichnung) for e in Zaehler.query.all()]

        
class DeleteZaehler(FlaskForm):
    zaehler = SelectField('Zaehler', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zaehler.choices = [(str(e.id), e.bezeichnung) for e in Zaehler.query.all()]


class AddZaehlertyp(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        typ = Zaehlertypen.query.filter_by(bezeichnung=bezeichnung.data).first()
        if typ:
            raise ValidationError("Diesen Zählertyp gibt es schon!")


class EditZaehlertypen(FlaskForm):
    zaehlertypen = SelectField('Zaehlertypen', choices=[], validators=[DataRequired()])
    bezeichnung = StringField('Bezeichnung', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Speichern')

    def __init__(self, *args, **kwargs):
        super(EditZaehlertypen, self).__init__(*args, **kwargs)
        self.zaehlertypen.choices = [(e.id, e.bezeichnung) for e in Zaehlertypen.query.all()]

        
class DeleteZaehlertypen(FlaskForm):
    zaehlertypen = SelectField('Zaehlertypen', choices=[], validators=[DataRequired()])
    submit = SubmitField('Löschen')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zaehlertypen.choices = [(str(e.id), e.bezeichnung) for e in Zaehlertypen.query.all()]
        

class AddVermietung(FlaskForm):
    weid = StringField("WEID", validators=[DataRequired(), Length(max=5)])
    wohnung = StringField("Wohnung", validators=[DataRequired(), Length(max=4)])
    vorname = StringField("Vorname", validators=[DataRequired(), Length(max=20)])
    nachname = StringField("Nachname", validators=[DataRequired(), Length(max=20)])
    strasse = StringField("Straße", validators=[DataRequired(), Length(max=30)])
    hausnummer = StringField("Hausnummer", validators=[DataRequired(), Length(max=4)])
    plz = StringField("Postleitzahl", validators=[DataRequired(), Length(max=5)])
    ort = StringField("Ort", validators=[DataRequired(), Length(max=30)])
    mietbeginn = DateField("Mietbeginn", validators=[DataRequired()])
    mietende = DateField("Mietende")
    personen = StringField("Personen", validators=[DataRequired(), Length(max=2)])
    submit = SubmitField("Speichern")

    def validate_weid(self, weid):
        weid = Vermietung.query.filter_by(weid=weid.data).first()
        if weid:
            raise ValidationError("Diese WEID gibt es schon!")
