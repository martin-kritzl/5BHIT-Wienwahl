from shutil import copyfile
import unittest

from csv.CSVHandler import CSVHandler

__author__ = 'mkritzl'

class TestCSV(unittest.TestCase):

    def setUp(self):
        copyfile("../resource/data.csv", "../resource/test.csv")
        self.csvHandler = CSVHandler()
        self.csvHandler.clearFile("../resource/data.csv", "../resource/test.csv")

    def testReadAllString(self):
        self.assertTrue("4;1;1;1;0;0;80;4;27;14;15;10;9;0;1;0;0;0;0;0\r\n" in self.csvHandler.getContentAsString("../resource/test.csv"))

    def testReadAllArray(self):
        self.assertEquals("715",self.csvHandler.getContentAsArray("../resource/test.csv")[2][5])

    def testGetLine(self):
        self.assertEqual("4;1;1;1;1;715;387;10;128;86;75;40;44;0;4;0;0;0;0;0", self.csvHandler.getLineAsString("../resource/test.csv", 3))

    def testAppendLine(self):
        self.csvHandler.appendLine("../resource/test.csv", "Neue Zeile;1")
        self.csvHandler.appendLine("../resource/test.csv", ["Neue Zeile", "2"])
        self.assertEqual("Neue Zeile;1", self.csvHandler.getLineAsString("../resource/test.csv", 1547))
        self.assertEqual("Neue Zeile;2", self.csvHandler.getLineAsString("../resource/test.csv", 1548))

    def testSetContent(self):
        self.csvHandler.setVotes("../resource/test.csv", "Das ist alles")
        self.assertEquals("Das ist alles\r\n", self.csvHandler.getContentAsString("test.csv"))
