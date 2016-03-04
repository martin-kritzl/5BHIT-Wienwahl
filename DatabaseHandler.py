from itertools import chain
from unittest.mock import Base
from sqlalchemy import create_engine, select
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
        for row in self.conn.execute(select([wahlstimmen]).where(wahlstimmen.wahltermin == wahltermin)):
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
        for row in self.conn.execute(select([parteistimmen]).where(parteistimmen.wahltermin == wahltermin).where(parteistimmen.bezirknr == bezirk).where(parteistimmen.sprengelnr == sprengel)):
            stimmen.append([row.parteiname, row.menge])
        return stimmen


    def getConentAsArray(self, accessor):
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


    def setContent(self, content, accessor):





