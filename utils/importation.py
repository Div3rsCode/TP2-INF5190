
import urllib.request
import urllib.parse
import pandas
import xml.etree.ElementTree

# puisque je fais confiance à la ville de Montréal,
# j'ai décidé d'ignorer les vulnérabilités XML.


def piscine_to_DF(url):
    colonnes_csv = ['ID_UEV', 'TYPE_INSTALLATION',
                    'NOM_INSTALLATION', 'ARRONDISSEMENT', 'ADRESSE',
                    'PROPRIETE', 'GESTION', 'POINT_X', 'POINT_Y',
                    'EQUIPEMENT', 'LONGITUDE', 'LATITUDE']
    csv_df = pandas.read_csv(url, header=0, names=colonnes_csv,
                             encoding="utf-8")
    return csv_df.sort_values(by='ARRONDISSEMENT')


def patinoire_to_DF(url):
    donnees = urllib.request.urlopen(url).read().decode("utf-8")
    xml_file = xml.etree.ElementTree.fromstring(donnees)
    colonnes = ["ARRONDISSEMENT", "NOM_INSTALLATION", "DATE_MAJ",
                "OUVERT", "DEBLAYE", "ARROSE", "RESURFACE"]
    lignes = []
    for node in xml_file:
        for node2 in node.iter("patinoire"):
            for node3 in node2.iter("condition"):
                nom_arr = node.find("nom_arr").text.strip()
                nom_pat = node2.find("nom_pat").text.strip().replace("()", "")
                date_heure = node3.find("date_heure").text.strip()
                ouvert = node3.find("ouvert").text.strip()
                deblaye = node3.find("deblaye").text.strip()
                arrose = node3.find("arrose").text.strip()
                resurface = node3.find("resurface").text.strip()
                lignes.append({"ARRONDISSEMENT": nom_arr,
                               "NOM_INSTALLATION": nom_pat,
                               "DATE_MAJ": date_heure,
                               "OUVERT": ouvert,
                               "DEBLAYE": deblaye,
                               "ARROSE": arrose,
                               "RESURFACE": resurface})
    xml_df = pandas.DataFrame(lignes, columns=colonnes)

    return xml_df.drop_duplicates(subset=['ARRONDISSEMENT'], keep='last')


def glissade_to_DF(url):
    donnees = urllib.request.urlopen(url).read().decode("utf-8")
    xml_file = xml.etree.ElementTree.fromstring(donnees)
    colonnes = ["NOM_INSTALLATION", "ARRONDISSEMENT", "CODE_ARR",
                "DATE_MAJ", "OUVERT", "DEBLAYE", "CONDITION"]
    lignes = []
    for node in xml_file:
        nom = node.find("nom").text
        nom_arr = node.find("arrondissement").find("nom_arr").text
        code_arr = node.find("arrondissement").find("cle").text
        date_maj = node.find("arrondissement").find("date_maj").text
        ouvert = node.find("ouvert").text if node is not None else None
        deblayee = node.find("deblaye").text if node is not None else None
        condition = node.find("condition").text
        lignes.append({"NOM_INSTALLATION": nom,
                       "ARRONDISSEMENT": nom_arr,
                       "CODE_ARR": code_arr,
                       "DATE_MAJ": date_maj,
                       "OUVERT": ouvert,
                       "DEBLAYE": deblayee,
                       "CONDITION": condition})

    xml_df = pandas.DataFrame(lignes, columns=colonnes)
    return xml_df.sort_values(by='ARRONDISSEMENT')
