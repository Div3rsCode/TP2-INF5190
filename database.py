import sqlite3
import string
import pandas


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def inserer_donnees_SQL(self, donnees_DF: pandas.DataFrame, table: string):
        connection = sqlite3.connect('db/database.db')
        donnees_DF.to_sql(table, connection,
                          index_label='id', if_exists='replace')

    def recevoir_donnees_SQL(self, table: string):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM %s" % (table))
        donnees = cursor.fetchall()
        colonnes = []
        for nom in cursor.description:
            colonnes.append(nom[0])
        return (colonnes, donnees)

    def inserer_arrondissement_SQL(self, df1, df2, df3):
        df_final = pandas.concat(
            [df1['ARRONDISSEMENT'], df2['ARRONDISSEMENT'],
             df3['ARRONDISSEMENT']])
        df_final = df_final.drop_duplicates()
        connection = sqlite3.connect('db/database.db')
        df_final.to_sql('arrondissement', connection,
                        index_label='id', if_exists='replace')

    def get_installation_arr(self, arrondissement):
        cursor = self.get_connection().cursor()
        arrondissement = "%"+arrondissement+"%"
        cursor.execute(
            "SELECT nom_installation FROM piscine "
            "WHERE arrondissement like (?)"
            " UNION "
            "SELECT nom_installation FROM patinoire "
            "WHERE arrondissement like (?)"
            " UNION "
            "SELECT nom_installation FROM glissade "
            "WHERE arrondissement like (?)", (arrondissement, arrondissement,
                                              arrondissement))
        donnees = cursor.fetchall()
        return donnees

    def get_arrondissement(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT * "
            "FROM arrondissement")
        arrondissements = cursor.fetchall()
        return arrondissements

    def modifier_glissade(self, informations):
        nom_installation = informations['nom_installation']
        ouvert = informations['ouvert']
        deblaye = informations['deblaye']
        condition = informations['condition']
        cursor = self.get_connection().cursor()
        cursor.executescript("UPDATE glissade SET date_maj=date(), "
                             "ouvert={}, deblaye={}, condition={} "
                             "WHERE nom_installation "
                             "= {}; SELECT changes();".format(
                                 ouvert, deblaye, condition, nom_installation))
        est_modifie = int(cursor.fetchall())
        if est_modifie > 0:
            return True
        return False
