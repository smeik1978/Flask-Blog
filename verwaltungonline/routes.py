from crypt import methods
from curses import keyname
from datetime import datetime
import os
import json
from pyexpat.errors import messages
import secrets
from select import select
from wsgiref.util import request_uri
from PIL import Image
from attr import validate
#from sqlalchemy import text, create_engine
from traitlets import default
from sqlalchemy.orm import class_mapper, scoped_session, sessionmaker
import verwaltungonline.models as models
from flask import (
    get_flashed_messages,
    render_template,
    url_for,
    flash,
    redirect,
    request,
    abort,
    current_app,
    jsonify
)
from verwaltungonline import app, db, bcrypt
from verwaltungonline.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    frmAblesung,
    AddEinheit,
    AddGemeinschaft,
    AddKostenart,
    AddStockwerk,
    AddUmlageschluessel,
    AddWohnung,
    AddZaehler,
    AddZaehlertyp,
    EditEinheit,
    DeleteEinheit,
    EditGemeinschaft,
    DeleteGemeinschaft,
    EditKostenarten,
    DeleteKostenarten,
    EditStockwerke,
    DeleteStockwerke,
    EditUmlageschluessel,
    DeleteUmlageschluessel,
    EditWohnungen,
    DeleteWohnungen,
    EditZaehler,
    DeleteZaehler,
    EditZaehlertypen,
    DeleteZaehlertypen,
    AddKosten,
    EditKosten,
    DeleteKosten,
    AddVermietung,
    EditVermietung,
    DeleteVermietung,
)
from verwaltungonline.models import (
    User,
    Post,
    Ablesung,
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
from .modules import query_models


# Funktionen für Seiten


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)


@app.route("/ablesung", methods=["GET", "POST"])
@login_required
def ablesung():
    form = frmAblesung()
    ablesung = Ablesung.query.all()
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Vermietung.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    print(f"row_dict: {row_dict}")
                    wohnung_zaehler = Zaehler.query.filter_by(wohnung_id=row_dict["wohnung_id"]).all()
                    print(f"wohnung_zaehler: {wohnung_zaehler}")
                    wohnung_zaehler_nummer = {}
                    i=1
                    for item in wohnung_zaehler:
                        wohnung_zaehler_nummer[i]=item.nummer
                        i +=1
                    print(f"wohnung_zaehler_nummer: {wohnung_zaehler_nummer}")
                    del row_dict['_sa_instance_state']
                    row_dict['Mietbeginn'] = row_dict['mietbeginn'].strftime('%Y-%m-%d')
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    for key in row_dict.keys():
                        pass
                        #print(f"Key: {key}")
                    #json_data = json.dumps(row_dict, default=str)
                    json_data = json.dumps(wohnung_zaehler_nummer, default=str)
                    print(f"JSON to send: {json_data}")
                    return json_data
    return render_template(
        "ablesung.html",
        title="Ablesung",
        form=form,
        legend = "Ablesung",
        action=url_for("ablesung"),
        ablesung=ablesung
    )


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/einheiten")
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
        action=url_for("add_einheiten"),
    )


@app.route("/edit_einheiten", methods=["GET", "POST"])
def edit_einheiten():
    form = EditEinheit()
    einheit = Einheiten.query.get(form.einheit.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Einheiten.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Einheit gibt es schon!")
            return redirect(url_for("einheiten"))
        einheit.bezeichnung = bezeichnung
        db.session.commit()
        flash("Einheit erfolgreich aktualisiert!")
        return redirect(url_for("einheiten"))
    else:
        print(form.errors)
    return render_template(
        "edit_einheiten.html",
        form=form,
        legend="Einheit bearbeiten",
        action=url_for("edit_einheiten"),
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
        return redirect(url_for("einheiten"))

    return render_template(
        "delete_einheiten.html",
        form=form,
        legend="Einheit löschen",
        action=url_for("delete_einheiten"),
    )


@app.route("/Gemeinschaft")
@login_required
def gemeinschaft():
    gemeinschaft = Gemeinschaft.query.all()
    return render_template(
        "gemeinschaft.html", title="Gemeinschaftsflächen", gemeinschaft=gemeinschaft
    )


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


@app.route("/edit_gemeinschaft", methods=["GET", "POST"])
def edit_gemeinschaft():
    form = EditGemeinschaft()
    gemeinschaft = Gemeinschaft.query.get(form.gemeinschaft.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Gemeinschaft.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Gemeinschaftsfläche gibt es schon!")
            return redirect(url_for("gemeinschaft"))
        gemeinschaft.bezeichnung = bezeichnung
        db.session.commit()
        flash("Datensatz erfolgreich aktualisiert!")
        return redirect(url_for("gemeinschaft"))
    else:
        print(form.errors)
    return render_template(
        "edit_gemeinschaft.html",
        form=form,
        legend="Datensatz bearbeiten",
        action=url_for("edit_gemeinschaft"),
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
        return redirect(url_for("gemeinschaft"))

    return render_template(
        "delete_gemeinschaft.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_gemeinschaft"),
    )


@app.route("/kosten")
@login_required
def kosten():
    #kosten = Kosten.query.all()
    kosten = Kosten.query.options(db.joinedload(Kosten.kostenart), db.joinedload(Kosten.einheit), db.joinedload(Kosten.umlageschluessel)).all()
    columns = Kosten.__table__.columns.keys()
    column_names = [column[:-3].capitalize() if column.endswith('_id') else column.capitalize() for column in columns if column != 'id']
    return render_template("kosten.html", title="Kosten", kosten=kosten, column_names=column_names)


@app.route("/add_kosten", methods=["GET", "POST"])
@login_required
def add_kosten():
    form = AddKosten()
    if form.validate_on_submit():
        kosten = Kosten(
            datum=form.datum.data,
            abrechnungsjahr=form.abrechnungsjahr.data,
            kostenarten_id=form.kostenart.data,
            firma=form.firma.data,
            leistung=form.leistung.data,
            betrag=form.betrag.data,
            menge=form.menge.data,
            einheiten_id=form.einheit.data,
            umlageschluessel_id=form.umlageschluessel.data,
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


@app.route("/edit_kosten", methods=["GET", "POST"])
@login_required
def edit_kosten():
    form = EditKosten()
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Kosten.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    del row_dict['_sa_instance_state']
                    row_dict['Datum'] = row_dict['datum'].strftime('%Y-%m-%d')
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    json_data = json.dumps(row_dict, default=str)
                    return json_data
        else:
            if form.validate_on_submit():
                check = Kosten.query.filter_by(id=form.selleistung.data).first()
                if Kosten.query.filter_by(leistung=check.leistung).first() and form.leistung.data != check.leistung:
                    flash("Diese Leistung gibt es schon!")
                else:
                    row = Kosten.query.filter_by(id=form.selleistung.data).first()
                    if row:
                        row.datum = form.datum.data
                        row.abrechnungsjahr = form.abrechnungsjahr.data
                        row.kostenarten_id = form.kostenarten.data
                        row.firma = form.firma.data
                        row.leistung = form.leistung.data
                        row.betrag = form.betrag.data
                        row.menge = form.menge.data
                        row.einheiten_id = form.einheiten.data
                        row.umlageschluessel_id = form.umlageschluessel.data
                        db.session.commit()
                        flash("Kosten erfolgreich aktualisiert!")
                        return redirect(url_for("kosten"))
                    else:
                        flash("Keine Daten gefunden")
                        return redirect(url_for("kosten"))
            else:
                print('Form errors: ', form.errors)
    return render_template(
        "edit_kosten.html",
        form=form,
        legend="Kosten bearbeiten",
        action=url_for("edit_kosten"),
    )


@app.route("/delete_kosten", methods=["GET", "POST"])
@login_required
def delete_kosten():
    form = DeleteKosten()
    if form.validate_on_submit():
        kosten = Kosten.query.get(form.leistung.data)
        db.session.delete(kosten)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for("kosten"))

    return render_template(
        "delete_kosten.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_kosten"),
    )

@app.route("/kostenarten")
@login_required
def kostenarten():
    kostenarten = Kostenarten.query.all()
    return render_template(
        "kostenarten.html", title="Kostenarten", kostenarten=kostenarten
    )


@app.route("/add_kostenarten", methods=["GET", "POST"])
@login_required
def add_kostenarten():
    form = AddKostenart()
    if form.validate_on_submit():
        post = Kostenarten(bezeichnung=form.bezeichnung.data)
        db.session.add(post)
        db.session.commit()
        flash("Datensatz wurde angelegt.", "success")
        return redirect(url_for("kostenarten"))
    return render_template(
        "add_kostenarten.html",
        title="Kostenart hinzufügen",
        form=form,
        legend="Kostenart hinzufügen",
    )


@app.route("/edit_kostenarten", methods=["GET", "POST"])
def edit_kostenarten():
    form = EditKostenarten()
    kostenarten = Kostenarten.query.get(form.kostenarten.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Kostenarten.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Kostenart gibt es schon!")
            return redirect(url_for("kostenarten"))
        kostenarten.bezeichnung = bezeichnung
        db.session.commit()
        flash("Kostenart erfolgreich aktualisiert!")
        return redirect(url_for("kostenarten"))
    else:
        print(form.errors)
    return render_template(
        "edit_kostenarten.html",
        form=form,
        legend="Kostenarten bearbeiten",
        action=url_for("edit_kostenarten"),
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
        return redirect(url_for("kostenarten"))

    return render_template(
        "delete_kostenarten.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_kostenarten"),
    )


@app.route("/stammdaten")
@login_required
def stammdaten():
    return render_template("stammdaten.html")


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


@app.route("/edit_stockwerke", methods=["GET", "POST"])
def edit_stockwerke():
    form = EditStockwerke()
    stockwerke = Stockwerke.query.get(form.stockwerke.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Stockwerke.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diese Kostenart gibt es schon!")
            return redirect(url_for("kostenarten"))
        stockwerke.bezeichnung = bezeichnung
        db.session.commit()
        flash("Stockwerk erfolgreich aktualisiert!")
        return redirect(url_for("stockwerke"))
    else:
        print(form.errors)
    return render_template(
        "edit_stockwerke.html",
        form=form,
        legend="Stockwerke bearbeiten",
        action=url_for("edit_stockwerke"),
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
        return redirect(url_for("stockwerke"))

    return render_template(
        "delete_stockwerke.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_stockwerke"),
    )


@app.route("/umlageschluessel")
@login_required
def umlageschluessel():
    schluessel = Umlageschluessel.query.all()
    return render_template(
        "umlageschluessel.html", title="Umlageschlüssel", schluessel=schluessel
    )


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


@app.route("/edit_umlageschluessel", methods=["GET", "POST"])
def edit_umlageschluessel():
    form = EditUmlageschluessel()
    # umlageschluessel = Umlageschluessel.query.get(form.data)
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
        return redirect(url_for("umlageschluessel"))
    else:
        print(form.errors)
    return render_template(
        "edit_umlageschluessel.html",
        form=form,
        legend="Umlageschluessel bearbeiten",
        action=url_for("edit_umlageschluessel"),
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
        return redirect(url_for("umlageschluessel"))

    return render_template(
        "delete_umlageschluessel.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_umlageschluessel"),
    )


@app.route("/vermietung")
@login_required
def vermietung():
    #bezeichnungen = Vermietung.query.all()
    vermietung = Vermietung.query.options(db.joinedload(Vermietung.wohnung)).all()
    columns = Vermietung.__table__.columns.keys()
    column_names = [column[:-3].capitalize() if column.endswith('_id') else column.capitalize() for column in columns if column != 'id']
    return render_template(
        "vermietung.html", title="Vermietung", vermietung=vermietung, column_names=column_names)


@app.route("/add_vermietung", methods=["GET", "POST"])
@login_required
def add_vermietung():
    form = AddVermietung()
    if form.validate_on_submit():
        post = Vermietung(
            weid=form.weid.data,
            wohnung_id=form.wohnung.data,
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
    else:
        print('Form errors: ', form.errors)
    return render_template(
        "add_vermietung.html",
        title="Neue Mieter*in hinzufügen",
        form=form,
        legend="Neue Vermietung",
    )


@app.route("/edit_vermietung", methods=["GET", "POST"])
@login_required
def edit_vermietung():
    form = EditVermietung()
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Vermietung.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    del row_dict['_sa_instance_state']
                    row_dict['Mietbeginn'] = row_dict['mietbeginn'].strftime('%Y-%m-%d')
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    json_data = json.dumps(row_dict, default=str)
                    return json_data
        else:
            if form.validate_on_submit():
                check = Vermietung.query.filter_by(id=form.selweid.data).first()
                if Vermietung.query.filter_by(weid=form.weid.data).first() and form.weid.data != check.weid:
                    flash("Diese Nummer gibt es schon!")
                else:
                    row = Vermietung.query.filter_by(id=form.selweid.data).first()
                    print(f'form.wohnung.data: {form.wohnung.data}')
                    if row:
                        row_dict = row.__dict__
                        for key in row_dict.keys():
                            print(key)
                        row.weid = form.weid.data
                        row.wohnung_id = form.wohnung.data
                        row.vorname = form.vorname.data
                        row.nachname = form.nachname.data
                        row.strasse = form.strasse.data
                        row.hausnummer = form.hausnummer.data
                        row.plz = form.plz.data
                        row.ort = form.ort.data
                        row.mietbeginn = form.mietbeginn.data
                        row.mietende=form.mietende.data
                        row.personen=form.personen.data
                        db.session.commit()
                        flash("Datensatz erfolgreich aktualisiert!")
                        return redirect(url_for("vermietung"))
                    else:
                        flash("Keine Daten gefunden")
                        return redirect(url_for("vermietung"))
            else:
                print('Form errors: ', form.errors)
    return render_template(
        "edit_vermietung.html",
        form=form,
        legend="Vermietung bearbeiten",
        action=url_for("edit_vermietung"),
    )


@app.route("/delete_vermietung", methods=["GET", "POST"])
@login_required
def delete_vermietung():
    form = DeleteVermietung(request.form, validate_on_submit=False)
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Vermietung.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    del row_dict['_sa_instance_state']
                    row_dict['Mietbeginn'] = row_dict['mietbeginn'].strftime('%Y-%m-%d')
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    json_data = json.dumps(row_dict, default=str)
                    return json_data
        else:
            weid = Vermietung.query.get(form.weid.data)
            db.session.delete(weid)
            db.session.commit()
            flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
            return redirect(url_for("vermietung"))
    return render_template(
        "delete_vermietung.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_vermietung"),
    )


@app.route("/verwaltung")
@login_required
def verwaltung():
    return render_template("verwaltung.html", title="Verwaltung")


@app.route("/wohnungen")
@login_required
def wohnungen():
    #wohnungen = Wohnungen.query.all()
    #wohnungen = Wohnungen.query.join(Stockwerke, Wohnungen.stockwerk==Stockwerke.id).add_columns(Wohnungen.nummer, Stockwerke.bezeichnung as stockwerk, Wohnungen.qm, Wohnungen.zimmer).all()
    wohnungen = Wohnungen.query.options(db.joinedload(Wohnungen.stockwerk)).all()

    print(wohnungen)
    return render_template("wohnungen.html", title="Wohnungen", wohnungen=wohnungen)


@app.route("/add_wohnung", methods=["GET", "POST"])
@login_required
def add_wohnung():
    form = AddWohnung()
    if form.validate_on_submit():
        post = Wohnungen(
            nummer=form.nummer.data,
            stockwerk_id=form.stockwerk.data,
            qm=form.qm.data,
            zimmer=form.zimmer.data,
        )
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


@app.route("/edit_wohnungen", methods=["GET", "POST"])
@login_required
def edit_wohnungen():
    form = EditWohnungen()
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Wohnungen.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    del row_dict['_sa_instance_state']
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    json_data = json.dumps(row_dict, default=str)
                    return json_data
        else:
            if form.validate_on_submit():
                check = Wohnungen.query.filter_by(id=form.selnummer.data).first()
                if Wohnungen.query.filter_by(nummer=form.nummer.data).first() and form.nummer.data != check.nummer:
                    flash("Diese Nummer gibt es schon!")
                else:
                    row = Wohnungen.query.filter_by(id=form.selnummer.data).first()
                    print(row)
                    if row:
                        row.nummer = form.nummer.data
                        row.stockwerk_id = form.stockwerk.data
                        row.qm = form.qm.data
                        row.zimmer = form.zimmer.data
                        db.session.commit()
                        flash("Wohnung erfolgreich aktualisiert!")
                        return redirect(url_for("wohnungen"))
                    else:
                        flash("Keine Daten gefunden")
                        return redirect(url_for("wohnungen"))
            else:
                print('Form errors: ', form.errors)
    return render_template(
        "edit_wohnungen.html",
        form=form,
        legend="Wohnungen bearbeiten",
        action=url_for("edit_wohnungen"),
    )


@app.route("/delete_wohnungen", methods=["GET", "POST"])
@login_required
def delete_wohnungen():
    form = DeleteWohnungen()
    if form.validate_on_submit():
        wohnungen = Wohnungen.query.get(form.nummer.data)
        db.session.delete(wohnungen)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for("wohnungen"))

    return render_template(
        "delete_wohnungen.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_wohnungen"),
    )

@app.route("/zaehler")
@login_required
def zaehler():
    #zaehler = Zaehler.query.all()
    zaehler = Zaehler.query.options(db.joinedload(Zaehler.typ), db.joinedload(Zaehler.wohnung)).all()
    return render_template("zaehler.html", title="Zähler", zaehler=zaehler)


@app.route("/add_zaehler", methods=["GET", "POST"])
@login_required
def add_zaehler():
    form = AddZaehler()
    if form.validate_on_submit():
        print(f"Typ: {form.typ.data}")
        print(f"Wohnung: {form.wohnung.data}")
        post = Zaehler(
            nummer=form.nummer.data,
            typ_id=form.typ.data,
            gemeinschaft=form.gemeinschaft.data,
            wohnung_id=form.wohnung.data,
            ort=form.ort.data,
        )
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


@app.route("/edit_zaehler", methods=["GET", "POST"])
@login_required
def edit_zaehler():
    form = EditZaehler()
    if request.method == "POST":
        if request.content_type == 'application/json':
            print(f"Gemeinschaft: {request.form.get('gemeinschaft')}")
            data = request.get_json()
            if data:
                print('JSON received: ', data)
                row = Zaehler.query.filter_by(id=data["id"]).first()
                if row:
                    row_dict = row.__dict__
                    del row_dict['_sa_instance_state']
                    row_dict[data['name']] = data['id']
                    keys_to_rename = []     # da die relevanten Datenbank-Spalten ein _id Suffix im Namen haben, müssen wir diese umbenennen
                    for key in row_dict.keys():
                        if key.endswith('_id'):
                            keys_to_rename.append(key)
                    for key in keys_to_rename:
                        new_key = key[:-3]
                        row_dict[new_key] = row_dict.pop(key)
                    json_data = json.dumps(row_dict, default=str)
                    return json_data
        else:
            if form.validate_on_submit():
                print(f"Gemeinschaft: {request.form.get('gemeinschaft')}")
                check = Zaehler.query.filter_by(id=form.selnummer.data).first()
                if Zaehler.query.filter_by(nummer=form.nummer.data).first() and form.nummer.data != check.nummer:
                    flash("Diese Nummer gibt es schon!")
                else:
                    row = Zaehler.query.filter_by(id=form.selnummer.data).first()
                    print(f"Gemeinschaft: {form.gemeinschaft.data}")
                    if row:
                        row.nummer = form.nummer.data
                        row.typ_id = form.typ.data
                        row.gemeinschaft = form.gemeinschaft.data
                        row.wohnung_id = form.wohnung.data
                        row.ort = form.ort.data
                        db.session.commit()
                        flash("Zähler erfolgreich aktualisiert!")
                        return redirect(url_for("zaehler"))
                    else:
                        flash("Keine Daten gefunden")
                        return redirect(url_for("zaehler"))
            else:
                print('Form errors: ', form.errors)
    return render_template(
        "edit_zaehler.html",
        form=form,
        legend="Zähler bearbeiten",
        action=url_for("edit_zaehler"),
    )

@app.route("/delete_zaehler", methods=["GET", "POST"])
@login_required
def delete_zaehler():
    form = DeleteZaehler()
    if form.validate_on_submit():
        zaehler = Zaehler.query.get(form.nummer.data)
        db.session.delete(zaehler)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for("zaehler"))

    return render_template(
        "delete_zaehler.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_zaehler"),
    )

@app.route("/zaehlertypen")
@login_required
def zaehlertypen():
    bezeichnung = Zaehlertypen.query.all()
    return render_template(
        "zaehlertypen.html", title="Zählertypen", bezeichnung=bezeichnung
    )


@app.route("/add_zaehlertypen", methods=["GET", "POST"])
@login_required
def add_zaehlertypen():
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


@app.route("/edit_zaehlertypen", methods=["GET", "POST"])
def edit_zaehlertypen():
    form = EditZaehlertypen()
    zaehlertypen = Zaehlertypen.query.get(form.zaehlertypen.data)
    if form.validate_on_submit():
        bezeichnung = form.bezeichnung.data
        if Zaehlertypen.query.filter_by(bezeichnung=bezeichnung).first():
            flash("Diesen Zählertyp gibt es schon!")
            return redirect(url_for("zaehlertypen"))
        zaehlertypen.bezeichnung = bezeichnung
        db.session.commit()
        flash("Zählertyp erfolgreich aktualisiert!")
        return redirect(url_for("zaehlertypen"))
    else:
        print(form.errors)
    return render_template(
        "edit_zaehlertypen.html",
        form=form,
        legend="zaehlertypen bearbeiten",
        action=url_for("edit_zaehlertypen"),
    )


@app.route("/delete_zaehlertypen", methods=["GET", "POST"])
@login_required
def delete_zaehlertypen():
    form = DeleteZaehlertypen()
    if form.validate_on_submit():
        zaehlertypen = Zaehlertypen.query.get(form.zaehlertypen.data)
        db.session.delete(zaehlertypen)
        db.session.commit()
        flash("Der Datensatz wurde erfolgreich gelöscht.", "success")
        return redirect(url_for("zaehlertypen"))

    return render_template(
        "delete_zaehlertypen.html",
        form=form,
        legend="Datensatz löschen",
        action=url_for("delete_zaehlertypen"),
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
        flash("Dein Konto wurde erstellt! Du kannst dich nun anmelden", "success")
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
            flash("Anmeldung fehlgeschlagen. Bitte prüfe Passwort und Email-Adresse", "danger")
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
        flash("Dein Konto wurde aktualisiert", "success")
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
        flash("Deine Nachricht wurde erstellt!", "success")
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
        flash("Deine Nachricht wurde aktualisiert!", "success")
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
    flash("Deine Nachricht wurde gelöscht!", "success")
    return redirect(url_for("home"))



