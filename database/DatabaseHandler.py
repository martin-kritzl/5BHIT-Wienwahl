from datetime import date, datetime
from itertools import chain
from unittest.mock import Base
from sqlalchemy import create_engine, select, delete, insert, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class DatabaseHandler(object):

    def __init__(self, databaseConnectionString):
        self.engine = create_engine(databaseConnectionString)
        self.conn = self.engine.connect()
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def getHeader(self, partein):
        header = ["T", "WV", "WK", "BZ", "SPR", "WBER", "ABG.", "UNG."]
        header = list(chain(header, partein))

        return header

    def getPartein(self, wahltermin):
        partein = []
        wahlstimmen = self.base.classes.wahlstimmen
        for row in self.engine.execute(select([wahlstimmen]).where(wahlstimmen.wahltermin == wahltermin).order_by(wahlstimmen.parteiname.asc())):
            partein.append(row.parteiname)

        return partein

    def getSprengel(self, wahltermin):
        sprengel = []

        result = self.engine.execute("SELECT 4, 1, wahlkreisnr, bezirknr, sprengelnr, wahlberechtigte, abgeg_stimmen, ung_stimmen FROM wahlkreis NATURAL JOIN bezirk NATURAL JOIN sprengel WHERE wahltermin='"+wahltermin+"'")
        for row in result:
            sprengel.append(list(row))
        return sprengel


    def getStimmen(self, wahltermin, bezirk, sprengel):
        stimmen = []
        parteistimmen = self.base.classes.parteistimmen
        for row in self.engine.execute(select([parteistimmen]).where(parteistimmen.wahltermin == wahltermin).where(parteistimmen.bezirknr == bezirk).where(parteistimmen.sprengelnr == sprengel)):
            stimmen.append([row.parteiname, row.menge])
        return stimmen


    def getVotesAsArray(self, accessor):
        if not accessor:
            return None
        content = []
        partein = self.getPartein(accessor)
        # content.append(self.getHeader(accessor))
        sprengel = self.getSprengel(accessor)
        appended = False
        for row in sprengel:
            stimmen = self.getStimmen(accessor, row[3], row[4])
            for partei in partein:
                for stimme in stimmen:
                    if (stimme[0]==partei):
                        row.append(stimme[1])
                        appended = True
                if appended==False:
                    row.append(None)
                    appended=True
        content.append(list(chain([self.getHeader(partein)], sprengel)))
        content = content[0]
        return content

    def getElections(self):
        elections = []
        wahl = self.base.classes.wahl
        for row in self.engine.execute(select([wahl])):
            elections.append(row.wahltermin.strftime("%Y-%m-%d"))

        return elections

    def deleteWahl(self, session, wahltermin):
        Sprengel = self.base.classes.sprengel
        Parteistimmen = self.base.classes.parteistimmen
        Wahlstimmen = self.base.classes.wahlstimmen

        session.query(Sprengel).filter(Sprengel.wahltermin == wahltermin).delete()
        session.query(Parteistimmen).filter(Parteistimmen.wahltermin == wahltermin).delete()
        session.query(Wahlstimmen).filter(Wahlstimmen.wahltermin == wahltermin).delete()

        # session.execute("DELETE FROM Parteistimmen WHERE wahltermin='" + wahltermin + "';")
        # session.execute("DELETE FROM Sprengel WHERE wahltermin='" + wahltermin + "';")
        # session.execute("DELETE FROM Wahlstimmen WHERE wahltermin='" + wahltermin + "';")

    def setContent(self, accessor,content,append):
        print("Set content")
        Wahl = self.base.classes.wahl
        Sprengel = self.base.classes.sprengel
        Parteistimmen = self.base.classes.parteistimmen

        s = Session(self.engine)
        try:
            if append==False:
                self.deleteWahl(s, accessor)
                print("Deleted content")

            exists = s.execute(select([Wahl]).where(Wahl.wahltermin==accessor))

            wahl_new = Wahl(wahltermin=accessor, mandate=None)

            if exists.rowcount==0:
                s.add(wahl_new)
            #
            #
            # s.commit()

            countpartei=8

            for row in content[1:]:
                sprengel_new = Sprengel(wahltermin=wahl_new.wahltermin, bezirknr=int(row[3]), sprengelnr=int(row[4]), wahlberechtigte=int(row[5]), abgeg_stimmen=int(row[6]), ung_stimmen=int(row[7]))
                s.add(sprengel_new)
                countpartei=8

                for act_partei in content[0][8:]:
                    parteistimmen_new = Parteistimmen(wahltermin=wahl_new.wahltermin, bezirknr=int(row[3]), sprengelnr=int(row[4]), parteiname=act_partei, menge=int(row[countpartei]))
                    s.add(parteistimmen_new)
                    countpartei+=1

            s.commit()


        except:
            s.rollback()
            raise
        finally:
            s.close()

    def createPrediction(self, wahltermin):
        time = datetime.now().strftime("%H:%M:%S")

        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        cursor.callproc("erzeugeHochrechnung", [wahltermin,time])
        cursor.close()
        connection.commit()

        return wahltermin

    def getPredictionsAsArray(self, wahltermin):
        time = datetime.now().strftime("%H:%M:%S")


        header = self.getPartein(wahltermin)
        header.insert(0, "Zeitpunkt")

        ergebnis = []
        ergebnis.append(header)
        hochrechnungsergebnis = self.base.classes.hochrechnungsergebnis
        hochrechnung = self.base.classes.hochrechnung


        for predictions in self.engine.execute(select([hochrechnung]).where(hochrechnung.wahltermin==wahltermin)):
            eineHochrechnung = []
            eineHochrechnung.append(predictions.zeitpunkt.strftime("%H:%M:%S"))
            for row in self.engine.execute(select([hochrechnungsergebnis]).where(hochrechnungsergebnis.wahltermin==predictions.wahltermin).where(hochrechnungsergebnis.zeitpunkt==predictions.zeitpunkt).order_by(hochrechnungsergebnis.parteiname.asc())):
                # partein.append(row.parteiname)
                eineHochrechnung.append(str(round(float(row.prozent), 3))+"%")
            ergebnis.append(eineHochrechnung)


        return ergebnis












