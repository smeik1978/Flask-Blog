from crypt import methods
import os
import re
import secrets
from wsgiref.util import request_uri
from PIL import Image
from sqlalchemy import text
from flask import render_template, url_for, flash, redirect, request, abort, jsonify, make_response, current_app
from verwaltungonline import app, db, bcrypt
from verwaltungonline.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    AddEinheit,
    AddGemeinschaft,
    AddKostenart,
    AddStockwerk,
    AddUmlageschluessel,
    AddVermietung,
    AddWohnung,
    AddZaehler,
    AddZaehlertyp,
)
from verwaltungonline.models import (
    User,
    Post,
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
def einheiten():
    return render_template("einheiten.html")

@app.route("/einheiten/add_einheit", methods=["GET", "POST"])
@login_required
def add_einheit():
    form = AddEinheit()
    if form.validate_on_submit():
        post = Einheiten(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stammdaten"))
    return render_template(
        "add_einheit.html",
        title="Einheit hinzufügen",
        form=form,
        legend="Einheit hinzufügen",
    )


@app.route("/gemeinschaft")
@login_required
def gemeinschaft():
    bezeichnungen = Gemeinschaft.query.all()
    return render_template(
        "stammdaten.html", title="Gemeinschaftsflächen", bezeichnungen=bezeichnungen
    )


@app.route("/gemeinschaft/add_gemeinschaft", methods=["GET", "POST"])
@login_required
def add_gemeinschaft():
    form = AddGemeinschaft()
    if form.validate_on_submit():
        post = Gemeinschaft(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stammdaten"))
    return render_template(
        "add_gemeinschaft.html",
        title="Fläche hinzufügen",
        form=form,
        legend="Fläche hinzufügen",
    )


@app.route("/kostenarten")
@login_required
def kostenarten():
    bezeichnungen = Kostenarten.query.all()
    return render_template(
        "gemeinschaft.html", title="Kostenarten", bezeichnungen=bezeichnungen
    )


@app.route("/kostenarten/add_kostenart", methods=["GET", "POST"])
@login_required
def add_kostenart():
    form = AddKostenart()
    if form.validate_on_submit():
        post = Kostenarten(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("kostenarten"))
    return render_template(
        "add_kostenart.html",
        title="Kostenart hinzufügen",
        form=form,
        legend="Kostenart hinzufügen",
    )


@app.route("/stammdaten", methods=["GET", "POST"])
@login_required
def stammdaten():
    einheiten = Einheiten.query.all()
    print(type(einheiten))
    return render_template(
        "stammdaten.html", einheiten=einheiten)

@app.route("/stammdaten/fill_tab", methods=["POST"])
#@login_required
def fill_tab():
    req = request.get_json()
    test = req.split("-")
    for t in db.metadata.tables.values():
        pass
    models = {
    mapper.class_.__name__
    for mapper in db.Model.registry.mappers
    }
    query = text("SELECT * FROM " + test[0])
    conn = db.engine.connect()
    result = conn.execute(query)
    for row in result:
        pass #print(row[1])
    
    res = make_response(jsonify({"message": "Data received"}), 200)
    return res
    
    
@app.route("/stockwerke")
@login_required
def stockwerke():
    bezeichnungen = Stockwerke.query.all()
    return render_template(
        "stockwerke.html", title="Stockwerke", bezeichnungen=bezeichnungen
    )


@app.route("/stockwerke/add_stockwerk", methods=["GET", "POST"])
@login_required
def add_stockwerk():
    form = AddStockwerk()
    if form.validate_on_submit():
        post = Stockwerke(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("stockwerke"))
    return render_template(
        "add_stockwerk.html",
        title="Stockwerk hinzufügen",
        form=form,
        legend="Stockwerk hinzufügen",
    )


@app.route("/umlageschluessel")
@login_required
def umlageschluessel():
    bezeichnungen = Umlageschluessel.query.all()
    return render_template(
        "umlageschluessel.html", title="Umlageschlüssel", bezeichnungen=bezeichnungen
    )


@app.route("/umlageschluessel/add_umlageschluessel", methods=["GET", "POST"])
@login_required
def add_umlageschluessel():
    form = AddUmlageschluessel()
    if form.validate_on_submit():
        post = Umlageschluessel(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("umlageschluessel"))
    return render_template(
        "add_umlageschluessel.html",
        title="Umlageschlüssel hinzufügen",
        form=form,
        legend="Umlageschlüssel hinzufügen",
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
    bezeichnungen = Wohnungen.query.all()
    return render_template(
        "wohnungen.html", title="Wohnungen", bezeichnungen=bezeichnungen
    )


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
    bezeichnungen = Zaehler.query.all()
    return render_template("zaehler.html", title="Zähler", bezeichnungen=bezeichnungen)


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
    bezeichnungen = Zaehlertypen.query.all()
    return render_template(
        "zaehlertypen.html", title="Zählertypen", bezeichnungen=bezeichnungen
    )


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
