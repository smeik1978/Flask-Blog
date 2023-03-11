from crypt import methods
from curses import keyname
import os
from pyexpat.errors import messages
import secrets
from wsgiref.util import request_uri
from PIL import Image
from sqlalchemy import text
from sqlalchemy.orm import class_mapper
from flask import get_flashed_messages, render_template, url_for, flash, redirect, request, abort, current_app, jsonify
from verwaltungonline import app, db, bcrypt
from verwaltungonline.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, PostForm,
    AddEinheit, AddGemeinschaft, AddKostenart, AddStockwerk, AddUmlageschluessel, AddVermietung, AddWohnung, AddZaehler, AddZaehlertyp,
    EditEinheit, DeleteEinheit, EditGemeinschaft, DeleteGemeinschaft, EditKostenarten, DeleteKostenarten, EditStockwerke, DeleteStockwerke,
    EditUmlageschluessel, DeleteUmlageschluessel, EditWohnungen, DeleteWohnungen, EditZaehler, DeleteZaehler, EditZaehlertypen, DeleteZaehlertypen,
    AddKosten, EditKosten, DeleteKosten
)
from verwaltungonline.models import (
    User,
    Post,
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
from flask_login import login_user, current_user, logout_user, login_required


# Funktionen für Seiten

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)




@app.route("/ablesung")
@login_required
def ablesung():
    bezeichnungen = Einheiten.query.all()
    return render_template(
        "ablesung.html", title="Ablesung", bezeichnungen=bezeichnungen
    )

@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route('/einheiten')
@login_required
def einheiten():
    einheiten = Einheiten.query.all()
    return render_template("einheiten.html", title="Einheiten", einheiten=einheiten)


@app.route("/add_einheiten", methods=["GET", "POST"])
@login_required
def add_einheiten():
    form = AddEinheit()
    if form.validate_on_submit():
        post = Einheiten(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stammdaten"))
    return render_template(
        "add_einheiten.html",
        title="Einheit hinzufügen",
        form=form,
        legend="Einheit hinzufügen",
        action=url_for('add_einheiten')
    )

@app.route('/edit_einheiten', methods=['GET', 'POST'])
def edit_einheiten():
    form = EditEinheit()
    einheit = Einheiten.query.get(form.einheit.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Einheiten.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Einheit gibt es schon!")
            return redirect(url_for('einheiten'))
        einheit.bezeichnung = bezeichnung
        db.session.commit()
        flash("Einheit erfolgreich aktualisiert!")
        return redirect(url_for('einheiten'))
    else:
        print(form.errors)
    return render_template(
        'edit_einheiten.html',
        form=form,
        legend="Einheit bearbeiten",
        action=url_for('edit_einheiten')
        )


@app.route("/delete_einheiten", methods=["GET", "POST"])
@login_required
def delete_einheiten():
    form = DeleteEinheit()
    if form.validate_on_submit():
        einheit = Einheiten.query.get(form.einheit.data)
        db.session.delete(einheit)
        db.session.commit()
        flash("Die Einheit wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('einheiten'))

    return render_template(
        "delete_einheiten.html",
        form=form,
        legend="Einheit löschen",
        action=url_for('delete_einheiten')
    )


@app.route("/Gemeinschaft")
@login_required
def gemeinschaft():
    gemeinschaft = Gemeinschaft.query.all()
    return render_template("gemeinschaft.html", title="Gemeinschaftslächen", gemeinschaft=gemeinschaft)


@app.route("/add_gemeinschaft", methods=["GET", "POST"])
@login_required
def add_gemeinschaft():
    form = AddGemeinschaft()
    if form.validate_on_submit():
        post = Gemeinschaft(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("gemeinschaft"))
    return render_template(
        "add_gemeinschaft.html",
        title="Fläche hinzufügen",
        form=form,
        legend="Fläche hinzufügen",
    )


@app.route('/edit_gemeinschaft', methods=['GET', 'POST'])
def edit_gemeinschaft():
    form = EditGemeinschaft()
    gemeinschaft = Gemeinschaft.query.get(form.gemeinschaft.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Gemeinschaft.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Gemeinschaftsfläche gibt es schon!")
            return redirect(url_for('gemeinschaft'))
        gemeinschaft.bezeichnung = bezeichnung
        db.session.commit()
        flash("Datensatz erfolgreich aktualisiert!")
        return redirect(url_for('gemeinschaft'))
    else:
        print(form.errors)
    return render_template(
        'edit_gemeinschaft.html',
        form=form,
        legend="Datensatz bearbeiten",
        action=url_for('edit_gemeinschaft')
        )


@app.route("/delete_gemeinschaft", methods=["GET", "POST"])
@login_required
def delete_gemeinschaft():
    form = DeleteGemeinschaft()
    if form.validate_on_submit():
        gemeinschaft = Gemeinschaft.query.get(form.gemeinschaft.data)
        db.session.delete(gemeinschaft)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('gemeinschaft'))

    return render_template(
        "delete_gemeinschaft.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for('delete_gemeinschaft')
    )


@app.route("/kosten")
@login_required
def kosten():
    kosten = Kosten.query.all()
    return render_template("kosten.html", title="Kosten", kosten=kosten)


@app.route("/add_kosten", methods=["GET", "POST"])
@login_required
def add_kosten():
    form = AddKosten()
    if form.validate_on_submit():
        kosten = Kosten(
            datum=form.datum.data,
            abrechnungsjahr=form.abrechnungsjahr.data,
            kostenart=form.kostenart.data,
            firma=form.firma.data,
            leistung=form.leistung.data,
            betrag=form.betrag.data,
            menge=form.menge.data,
            einheit=form.einheit.data,
            umlageschluessel=form.umlageschluessel.data,
        )
        db.session.add(kosten)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("kosten"))
    else:
        print(form.errors)
    return render_template(
        "add_kosten.html",
        title="Kosten hinzufügen",
        form=form,
        legend="Kosten hinzufügen",
    )


@app.route('/edit_kosten', methods=['GET', 'POST'])
def edit_kosten():
    form = EditKosten()
    kosten = Kosten.query.all()
    if form.validate_on_submit():
        kosten = form.kosten.data
        kosten = Kosten(
            datum=form.datum.data,
            abrechnungsjahr=form.abrechnungsjahr.data,
            kostenart=form.kostenart.data,
            # firma=form.firma.data,
            leistung=form.leistung.data,
            # betrag=form.betrag.data,
            # menge=form.menge.data,
            # einheit=form.einheit.data,
            # umlageschluessel=form.umlageschluessel.data,
        )
        if Kosten.query.filter_by(leistung=leistung).first():
            flash("Diese Kosten gibt es schon!")
            return redirect(url_for('kosten'))
        db.session.commit()
        flash("Kosten erfolgreich aktualisiert!")
        return redirect(url_for('kosten'))
    else:
        print(form.errors)
    return render_template(
        'edit_kosten.html',
        form=form,
        legend="Kosten bearbeiten",
        action=url_for('edit_kosten'),
        kosten=kosten
        )

@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    print(data)
    # Wir bekommen via json den Namen (nicht Inhalt) des selektierten Wertes (z.B. leistung oder kostenart) und dessen ID in der Select-Liste
    # Anhand des Namens müsste man das DB Model herausfinden und die Elemente loopen.
    # for element in elements: -> fülle die Liste mit elementname : qResult.elementname
    # Das müsste dann eine universellere Lösung zum Auslesen der Select-Fields sein.
    # data["abrechnungsjahr"] : qResult.abrechnungsjahr
    # same for JS :-/ , for each oder so
    qResult = Kosten.query.filter_by(id=data['id']).first()
    if qResult:
        data = {
            'abrechnungsjahr': qResult.abrechnungsjahr
        }

        return jsonify(data)
    else:
        return jsonify({'error': 'Kosten nicht gefunden'})



@app.route("/delete_kosten", methods=["GET", "POST"])
@login_required
def delete_kosten():
    form = DeleteKosten()
    if form.validate_on_submit():
        kosten = Kosten.query.get(form.kosten.data)
        db.session.delete(kosten)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('kosten'))

    return render_template(
        "delete_kosten.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for('delete_kosten')
    )


@app.route("/kostenarten")
@login_required
def kostenarten():
    kostenarten = Kostenarten.query.all()
    return render_template("kostenarten.html", title="Kostenarten", kostenarten=kostenarten)


@app.route("/add_kostenarten", methods=["GET", "POST"])
@login_required
def add_kostenarten():
    form = AddKostenart()
    if form.validate_on_submit():
        post = Kostenarten(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stammdaten"))
    return render_template(
        "add_kostenarten.html",
        title="Kostenart hinzufügen",
        form=form,
        legend="Kostenart hinzufügen",
    )


@app.route('/edit_kostenarten', methods=['GET', 'POST'])
def edit_kostenarten():
    form = EditKostenarten()
    kostenarten = Kostenarten.query.get(form.kostenarten.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Kostenarten.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Kostenart gibt es schon!")
            return redirect(url_for('kostenarten'))
        kostenarten.bezeichnung = bezeichnung
        db.session.commit()
        flash("Kostenart erfolgreich aktualisiert!")
        return redirect(url_for('kostenarten'))
    else:
        print(form.errors)
    return render_template(
        'edit_kostenarten.html',
        form=form,
        legend="Kostenarten bearbeiten",
        action=url_for('edit_kostenarten')
        )


@app.route("/delete_kostenarten", methods=["GET", "POST"])
@login_required
def delete_kostenarten():
    form = DeleteKostenarten()
    if form.validate_on_submit():
        kostenarten = Kostenarten.query.get(form.kostenarten.data)
        db.session.delete(kostenarten)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('kostenarten'))

    return render_template(
        "delete_kostenarten.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for('delete_kostenarten')
    )


@app.route("/stammdaten")
@login_required
def stammdaten():
    return render_template('stammdaten.html')


@app.route("/stockwerke")
@login_required
def stockwerke():
    stockwerke = Stockwerke.query.all()
    return render_template("stockwerke.html", title="Stockwerke", stockwerke=stockwerke)


@app.route("/add_stockwerke", methods=["GET", "POST"])
@login_required
def add_stockwerke():
    form = AddStockwerk()
    if form.validate_on_submit():
        post = Stockwerke(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stockwerke"))
    return render_template(
        "add_stockwerke.html",
        title="Stockwerk hinzufügen",
        form=form,
        legend="Stockwerk hinzufügen",
    )


@app.route('/edit_stockwerke', methods=['GET', 'POST'])
def edit_stockwerke():
    form = EditStockwerke()
    stockwerke = Stockwerke.query.get(form.stockwerke.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Stockwerke.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Kostenart gibt es schon!")
            return redirect(url_for('kostenarten'))
        stockwerke.bezeichnung = bezeichnung
        db.session.commit()
        flash("Stockwerk erfolgreich aktualisiert!")
        return redirect(url_for('stockwerke'))
    else:
        print(form.errors)
    return render_template(
        'edit_stockwerke.html',
        form=form,
        legend="Stockwerke bearbeiten",
        action=url_for('edit_stockwerke')
        )


@app.route("/delete_stockwerke", methods=["GET", "POST"])
@login_required
def delete_stockwerke():
    form = DeleteStockwerke()
    if form.validate_on_submit():
        stockwerke = Stockwerke.query.get(form.stockwerke.data)
        db.session.delete(stockwerke)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('stockwerke'))

    return render_template(
        "delete_stockwerke.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for('delete_stockwerke')
    )


@app.route("/umlageschluessel")
@login_required
def umlageschluessel():
    schluessel = Umlageschluessel.query.all()
    return render_template("umlageschluessel.html", title="Umlageschlüssel", schluessel=schluessel)

@app.route("/add_umlageschluessel", methods=["GET", "POST"])
@login_required
def add_umlageschluessel():
    form = AddUmlageschluessel()
    if form.validate_on_submit():
        umlageschluessel = Umlageschluessel(
            bezeichnung=form.bezeichnung.data,
            tabelle1=form.tabelle1.data,
            wert1=form.wert1.data,
            tabelle2=form.tabelle2.data,
            wert2=form.wert2.data,
            operation=form.operation.data,
        )
        db.session.add(umlageschluessel)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("umlageschluessel"))
    return render_template(
        "add_umlageschluessel.html",
        title="Umlageschlüssel hinzufügen",
        form=form,
        legend="Umlageschlüssel hinzufügen",
    )


@app.route('/edit_umlageschluessel', methods=['GET', 'POST'])
def edit_umlageschluessel():
    form = EditUmlageschluessel()
    #umlageschluessel = Umlageschluessel.query.get(form.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        # if Umlageschluessel.query.filter_by(bezeichnung=bezeichnung).first():
        #     flash("Diesen Schlüssel gibt es schon!")
        #     return redirect(url_for('umlageschluessel'))
        umlageschluessel = Umlageschluessel(
            bezeichnung=form.bezeichnung.data,
            tabelle1=form.tabelle1.data,
            wert1=form.wert1.data,
            tabelle2=form.tabelle2.data,
            wert2=form.wert2.data,
            operation=form.operation.data,
        )
        db.session.commit()
        flash("Schlüssel erfolgreich aktualisiert!")
        return redirect(url_for('umlageschluessel'))
    else:
        print(form.errors)
    return render_template(
        'edit_umlageschluessel.html',
        form=form,
        legend="Umlageschluessel bearbeiten",
        action=url_for('edit_umlageschluessel')
        )


@app.route("/delete_umlageschluessel", methods=["GET", "POST"])
@login_required
def delete_umlageschluessel():
    form = DeleteUmlageschluessel()
    if form.validate_on_submit():
        umlageschluessel = Umlageschluessel.query.get(form.umlageschluessel.data)
        db.session.delete(umlageschluessel)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for('umlageschluessel'))

    return render_template(
        "delete_umlageschluessel.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for('delete_umlageschluessel')
    )


@app.route("/vermietung")
@login_required
def vermietung():
    bezeichnungen = Vermietung.query.all()
    return render_template(
        "vermietung.html", title="Mieter*innen", bezeichnungen=bezeichnungen
    )


@app.route("/vermietung/add_vermietung", methods=["GET", "POST"])
@login_required
def add_vermietung():
    form = AddVermietung()
    if form.validate_on_submit():
        post = Vermietung(
            weid=form.weid.data,
            wohnung=form.wohnung.data,
            vorname=form.vorname.data,
            nachname=form.nachname.data,
            strasse=form.strasse.data,
            hausnummer=form.hausnummer.data,
            plz=form.plz.data,
            ort=form.ort.data,
            mietbeginn=form.mietbeginn.data,
            mietende=form.mietende.data,
            personen=form.personen.data,
        )
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("vermietung"))
    return render_template(
        "add_vermietung.html",
        title="Neue Mieter*in hinzufügen",
        form=form,
        legend="Neue Mieter*in hinzufügen",
    )

@app.route("/verwaltung")
def verwaltung():
    return render_template("verwaltung.html", title="Verwaltung")


@app.route("/wohnungen")
@login_required
def wohnungen():
    wohnungen = Wohnungen.query.all()
    return render_template("wohnungen.html", title="Wohnungen", wohnungen=wohnungen)

@app.route("/wohnungen/add_wohnung", methods=["GET", "POST"])
@login_required
def add_wohnung():
    form = AddWohnung()
    if form.validate_on_submit():
        post = Wohnungen(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("wohnungen"))
    return render_template(
        "add_wohnung.html",
        title="Wohnung hinzufügen",
        form=form,
        legend="Wohnung hinzufügen",
    )

@app.route("/zaehler")
@login_required
def zaehler():
    zaehler = Zaehler.query.all()
    return render_template("zaehler.html", title="Zähler", zaehler=zaehler)

@app.route("/zaehler/add_zaehler", methods=["GET", "POST"])
@login_required
def add_zaehler():
    form = AddZaehler()
    if form.validate_on_submit():
        post = Zaehler(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("zaehler"))
    return render_template(
        "add_zaehler.html",
        title="Zähler hinzufügen",
        form=form,
        legend="Zähler hinzufügen",
    )


@app.route("/zaehlertypen")
@login_required
def zaehlertypen():
    bezeichnung = Zaehlertypen.query.all()
    return render_template("zaehlertypen.html", title="Zählertypen", bezeichnung=bezeichnung)


@app.route("/zaehlertypen/add_zaehlertyp", methods=["GET", "POST"])
@login_required
def add_zaehlertyp():
    form = AddZaehlertyp()
    if form.validate_on_submit():
        post = Zaehlertypen(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("zaehlertypen"))
    return render_template(
        "add_zaehlertyp.html",
        title="Zählertyp hinzufügen",
        form=form,
        legend="Zählertyp hinzufügen",
    )

# Allgemeine Funktionen

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))
