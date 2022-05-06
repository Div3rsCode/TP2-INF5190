from distutils.log import error
import pandas
from .importation import *
from database import Database


def comparer_donnees_piscine(df: pandas.DataFrame, url):
    temp = piscine_to_DF(url)
    try:
        df.compare(temp)
    except error:
        db = Database()
        df = temp
        db.inserer_donnees_SQL(df, "piscine")
        db.disconnect()


def comparer_donnees_patinoire(df: pandas.DataFrame, url):
    temp = patinoire_to_DF(url)
    try:
        df.compare(temp)
    except error:
        db = Database()
        df = temp
        db.inserer_donnees_SQL(df, "patinoire")
        db.disconnect()


def comparer_donnees_glissade(df: pandas.DataFrame, url):
    temp = glissade_to_DF(url)
    try:
        df.compare(temp)
    except error:
        db = Database()
        df = temp
        db.inserer_donnees_SQL(df, "glissade")
        db.disconnect()
