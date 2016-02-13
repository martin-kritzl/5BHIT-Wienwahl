from shutil import copyfile
import unittest
from CSVHandler import CSVHandler

__author__ = 'mkritzl'

class TestCSV(unittest.TestCase):

    def setUp(self):
        copyfile("data.csv", "test.csv")
        self.csvHandler = CSVHandler("test.csv")
        self.csvHandler.clearFile("data.csv", "test.csv")

    def testReadAllString(self):
        self.assertTrue("4;1;1;1;0;0;80;4;27;14;15;10;9;0;1;0;0;0;0;0\r\n" in self.csvHandler.getContentAsString())

    def testReadAllArray(self):
        self.assertEquals("715",self.csvHandler.getContentAsArray()[2][5])

    def testGetLine(self):
        self.assertEqual("4;1;1;1;1;715;387;10;128;86;75;40;44;0;4;0;0;0;0;0", self.csvHandler.getLineAsString(3))

    def testAppendLine(self):
        self.csvHandler.appendLine("Neue Zeile;1")
        self.csvHandler.appendLine(["Neue Zeile", "2"])
        self.assertEqual("Neue Zeile;1", self.csvHandler.getLineAsString(1547))
        # self.assertEqual("Neue Zeile;2", self.csvHandler.getLineAsString(1548))
        self.assertEqual("Neue Zeile;2", self.csvHandler.getLineAsString(1548))

    def testSetContent(self):
        self.csvHandler.setContent("Das ist alles")
        self.assertEquals("Das ist alles\r\n", self.csvHandler.getContentAsString())
