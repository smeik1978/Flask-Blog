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
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from verwaltungonline.models import (
    User,
    Einheiten,
    Gemeinschaft,
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


class AddKostenart(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        kostenart = Kostenarten.query.filter_by(bezeichnung=bezeichnung.data).first()
        if kostenart:
            raise ValidationError("Diese Kostenart gibt es schon!")


class AddStockwerk(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        stockwerk = Stockwerke.query.filter_by(bezeichnung=bezeichnung.data).first()
        if stockwerk:
            raise ValidationError("Dieses Stockwerk gibt es schon!")


class AddUmlageschluessel(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        schluessel = Umlageschluessel.query.filter_by(
            bezeichnung=bezeichnung.data
        ).first()
        if schluessel:
            raise ValidationError("Diesen Schlüssel gibt es schon!")


class AddWohnung(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        wohnung = Wohnungen.query.filter_by(bezeichnung=bezeichnung.data).first()
        if wohnung:
            raise ValidationError("Diese Wohnung gibt es schon!")


class AddZaehler(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        zaehler = Zaehler.query.filter_by(bezeichnung=bezeichnung.data).first()
        if zaehler:
            raise ValidationError("Diesen Zähler gibt es schon!")


class AddZaehlertyp(FlaskForm):
    bezeichnung = StringField(
        "Bezeichnung", validators=[DataRequired(), Length(max=25)]
    )
    submit = SubmitField("Speichern")

    def validate_bezeichnung(self, bezeichnung):
        typ = Zaehlertypen.query.filter_by(bezeichnung=bezeichnung.data).first()
        if typ:
            raise ValidationError("Diesen Zählertyp gibt es schon!")


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
