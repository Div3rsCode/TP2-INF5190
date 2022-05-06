# -*- coding: utf-8 -*-
from utils.importation import *
from utils.verification import *
from utils.modification import *
from database import Database
from schemas import modifier_glissade_schema

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import jsonify
from flask_json_schema import JsonSchema

url1 = "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv"
url2 = "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml"
url3 = "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml"


projet = Flask(__name__)
schema = JsonSchema(projet)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# A1
data1 = piscine_to_DF(url1)
data2 = patinoire_to_DF(url2)
data3 = glissade_to_DF(url3)
db = Database()
db.inserer_donnees_SQL(data1, "piscine")
db.inserer_donnees_SQL(data2, "patinoire")
db.inserer_donnees_SQL(data3, "glissade")
db.inserer_arrondissement_SQL(data1, data2, data3)
# FIN A1


# A2
df_list = [data1, data2, data3]
url_list = [url1, url2, url3]
sched = BackgroundScheduler(timezone='UTC')
sched.add_job(comparer_donnees_piscine, 'cron', hour=0, args=[data1, url1])
sched.add_job(comparer_donnees_patinoire, 'cron', hour=0, args=[data2, url2])
sched.add_job(comparer_donnees_glissade, 'cron', hour=0, args=[data3, url3])
sched.start()
# FIN A2


@projet.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# A5
@projet.route('/', methods=['GET'])
def home():
    arrondissements = get_db().get_arrondissement()
    arrondissements = arrondissements
    return render_template('home.html', arrondissments=arrondissements)
# FIN A5


# A3
@projet.route('/doc', methods=['GET'])
def documentation():
    return render_template('doc.html')
# FIN A3


# A4 et C1
@projet.route('/api/installations', methods=['GET'])
def installations():
    if request.args.get('arrondissement'):
        nom_arr = request.args.get('arrondissement')
        if not nom_arr.isalpha():
            erreur = "Écrire un nom d'arrondissement"
            " valide (uniquement des lettres)."
            return render_template('erreur.html', erreur=erreur), 400
        else:
            liste_installations = get_db().get_installation_arr(nom_arr)
            liste_installations.pop(0)
            return jsonify(liste_installations), 200

    elif request.args.get('type'):
        type_installation = request.args.get('type')
        if type_installation not in ['glissade', 'patinoire', 'piscine']:
            erreur = "Veuillez entrer un type valide"
            " (patinoire, glissade ou piscine)."
            return render_template('erreur.html', erreur=erreur), 400

        else:
            informations = get_db().recevoir_donnees_SQL(type_installation)
            informations = to_list(informations, type_installation)
            return jsonify(informations), 200

    else:
        erreur = "Veuillez entrer comme paramêtre soit un "
        "arrondissement, soit un type d'installation."
        return render_template('erreur.html', erreur=erreur), 400
# FIN A4 et C1


# C3
@projet.route('/api/csv', methods=['GET'])
def donnees_csv():
    if request.args.get('type'):
        type_installation = request.args.get('type')
        if type_installation not in ['glissade', 'patinoire', 'piscine']:
            erreur = "Veuillez entrer un type valide"
            " (patinoire, glissade ou piscine)."
            return render_template('erreur.html', erreur=erreur), 400
        else:
            donnees = ""
            if type_installation == "piscine":
                donnees = data1.to_csv(index=False)
            elif type_installation == "glissade":
                donnees = data3.to_csv(index=False)
            elif type_installation == "patinoire":
                donnees = data2.to_csv(index=False)
            return donnees, 200

    else:
        erreur = "Veuillez entrer comme paramêtre un type d'installation."
        return render_template('erreur.html', erreur=erreur), 400
# FIN C3


# C2
@projet.route('/api/xml', methods=['GET'])
def donnees_xml():
    if request.args.get('type'):
        type_installation = request.args.get('type')
        if type_installation not in ['glissade',
                                     'patinoire', 'piscine']:
            erreur = "Veuillez entrer un type valide"
            " (patinoire, glissade ou piscine)."
            return render_template('erreur.html', erreur=erreur), 400
        else:
            donnees = ""
            if type_installation == "piscine":
                donnees = data1.to_xml(index=False)
            elif type_installation == "glissade":
                donnees = data3.to_xml(index=False)
            elif type_installation == "patinoire":
                donnees = data2.to_xml(index=False)
            return donnees, 200

    else:
        erreur = "Veuillez entrer comme paramètre "
        "soit un arrondissement, soit un type d'installation."
        return render_template('erreur.html', erreur=erreur), 400
# FIN C2


# D1
@projet.route('/api/glissade', methods=['PATCH'])
@schema.validate(modifier_glissade_schema)
def modifier_glissade():
    data = request.get_json()
    if get_db().modifier_glissade(data):
        message = "Les détails ont été modifiés"
        return render_template('confirmation.html', message=message), 200
    else:
        message = "La glissade n'a pas été trouvée."
        return render_template('confirmation.html', message=message), 400
# FIN D1
