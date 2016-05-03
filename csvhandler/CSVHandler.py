import csv

__author__ = 'mkritzl'

class CSVHandler(object):

    def getContentAsArray(self, file):
        with open(file, newline='') as csvfile:
            rows = []
            file = csv.reader(csvfile, delimiter=';')
            for row in file:
                rows.append(row[0:len(row)])
            return rows

    def setContent(self, file, content):
        with open(file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            csvfile.truncate()

            if isinstance(content, list):
                for row in content:
                    writer.writerow(row)