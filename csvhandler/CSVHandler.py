import collections
import csv
from itertools import islice

__author__ = 'mkritzl'

class CSVHandler(object):

    def getContentAsArray(self, file):
        with open(file, newline='') as csvfile:
            rows = []
            file = csv.reader(csvfile, delimiter=';')
            for row in file:
                rows.append(row[0:len(row)])
            return rows

    # def getContentAsString(self, file):
    #     output = ""
    #     rows = self.getContentAsArray(file)
    #     for row in rows:
    #         output = output + ';'.join(row[0:len(row)-1]) + '\r\n'
    #
    #     return output

    # def getLineAsArray(self, file, linenumber):
    #     linenumber = linenumber - 1
    #     with open(file, newline='') as csvfile:
    #         file = csv.reader(csvfile, delimiter=';')
    #         if linenumber is None:
    #             collections.deque(file, maxlen=0)
    #         else:
    #             next(islice(file, linenumber, linenumber), None)
    #
    #         return next(file)

    # def getLineAsString(self, file, linenumber):
    #     linenumber = linenumber - 1
    #     with open(file, newline='') as csvfile:
    #         file = csv.reader(csvfile, delimiter=';')
    #         if linenumber is None:
    #             collections.deque(file, maxlen=0)
    #         else:
    #             next(islice(file, linenumber, linenumber), None)
    #
    #
    #         tmp = next(file)
    #         return ';'.join(tmp)

    # def clearFile(self, fromFile, toFile):
    #     with open(fromFile, newline='') as csvSource, open(toFile, "w", newline='') as csvDest:
    #         reader = csv.reader(csvSource, delimiter=';')
    #         writer = csv.writer(csvDest, delimiter=';')
    #
    #         for row in reader:
    #             writer.writerow(row[0:len(row)-1])

    def setContent(self, file, content, *args):
        with open(file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            csvfile.truncate()

            if isinstance(content, list):
                for row in content:
                    # row.append("")
                    writer.writerow(row)
            # elif type(content) is str:
            #     writer.writerow(content.split(";"))

    # def appendLine(self, file, row):
    #     with open(file, "a", newline='') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=';')
    #
    #         if isinstance(row, list):
    #             writer.writerow(row)
    #         elif type(row) is str:
    #             writer.writerow(row.split(";"))