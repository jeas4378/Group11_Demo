import unittest
import os, sys
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__))+'/../src/')

import InformationLog as IL

class TestInformationLog(unittest.TestCase):

    def setUp(self):
        self.testLog = IL.InformationLog()

    def test_addInfo(self):
        # Några simpla test missingMunis:
        self.testLog.addInfo(missingMunis = "Sorsele")
        self.testLog.addInfo(missingMunis = "Övertorneå")
        self.testLog.addInfo(missingMunis = "Sorsele")
        # Inga dubletter, ok med åäö
        self.assertEqual(self.testLog._alertLog["missingMunis"], {"Sorsele","Övertorneå"})

        # Några simpla test missingData:
        self.testLog.addInfo(missingData = ("N15820", "2018"))
        self.testLog.addInfo(missingData = ("N15820", "2019"))
        self.testLog.addInfo(missingData = ("N15488", "2018"))
        # olika år läggs till listan, olika nyckeltal läggs som ny nyckel
        self.assertEqual(self.testLog._alertLog["missingData"], {"N15820":["2018","2019"],"N15488":["2018"]})
        # Olika fel
        with self.assertRaises(TypeError):
            self.testLog.addInfo(missingData=123)
            self.testLog.addInfo(missingData="ABC")

        # Några simpla test succeededYears
        self.testLog.addInfo(succeededYears = ("N15820", "2018"))
        self.testLog.addInfo(succeededYears = ("N15820", "2019"))
        self.testLog.addInfo(succeededYears = ("N15488", "2018"))
        # olika år läggs INTE till listan utan skriv över, olika nyckeltal läggs som ny nyckel
        self.assertEqual(self.testLog._alertLog["succeededYears"], {"N15820":"2019","N15488":"2018"})
        # olika fel
        with self.assertRaises(TypeError):
            self.testLog.addInfo(succeededYears=123)
            self.testLog.addInfo(succeededYears="ABC")

        # Några simpla test actualQty
        self.testLog.addInfo(actualQty = ("N15820", 55))
        self.testLog.addInfo(actualQty = ("N15820", 100))
        self.testLog.addInfo(actualQty = ("N15488", 55))
        # olika år läggs INTE till listan utan skriv över, olika nyckeltal läggs som ny nyckel
        self.assertEqual(self.testLog._alertLog["actualQty"], {"N15820":100,"N15488":55})
        # olika fel
        with self.assertRaises(TypeError):
            self.testLog.addInfo(actualQty=123)
            self.testLog.addInfo(actualQty="ABC")

        # Några för sekomCol och expectedTot, samt att flera grejer går att lägga samtidigt
        # den här typtestar inte infolog, så inte mycket annat att kolla
        self.testLog.addInfo(sekomCol = "Blå", expectedTot = 10)
        self.assertEqual(self.testLog._alertLog["sekomCol"],"Blå")
        self.assertEqual(self.testLog._alertLog["expectedTot"],10)

        # Ändrar vi nu är det ok
        self.testLog.addInfo(showSekomAvg = True)
        self.assertTrue(self.testLog._alertLog["showSekomAvg"])
        # men inte nu
        self.testLog.reset()
        with self.assertRaises(ValueError):
            self.testLog.addInfo(showSekomAvg = True)

        # fel med en felaktig nyckel
        with self.assertRaises(IndexError):
            self.testLog.addInfo(ABC = 123)


    def test_informUser(self):
        with self.assertRaises(IndexError):
            self.testLog.informUser("ABC")

        # lägg till lite att skriva ut
        self.testLog.addInfo(missingMunis = "Sorsele")
        self.testLog.addInfo(missingMunis = "Övertorneå")
        self.testLog.addInfo(missingMunis = "Kalix")
        self.testLog.addInfo(missingMunis = "Halmstad")
        self.testLog.addInfo(missingMunis = "Flen")
        self.testLog.addInfo(missingData = ("N15820", "2018"))
        self.testLog.addInfo(missingData = ("N15820", "2017"))
        self.testLog.addInfo(missingData = ("N15488", "2017"))
        self.testLog.addInfo(succeededYears = ("N15820", "2018"))
        self.testLog.addInfo(succeededYears = ("N15820", "2019"))
        self.testLog.addInfo(succeededYears = ("N15488", "2018"))
        self.testLog.addInfo(actualQty = ("N15820", 55))
        self.testLog.addInfo(actualQty = ("N15820", 60))
        self.testLog.addInfo(actualQty = ("N15488", 55))
        self.testLog.addInfo(sekomCol = "Blå", expectedTot = 60)
        self.testLog.addInfo(showSekomAvg = True)

        print("\nOBS KONTROLLERA MANUELLT:\n")
        print("\nInformera om att det saknas för flen:\n")
        self.testLog.informUser("missingMunis", kommun = "Flen")
        print("\nInformera om att det saknas för flera:\n")
        self.testLog.informUser("missingMunis", kommun = False)
        print("\nInformera inte om att det saknas för flen (tom rad korrekt):\n")
        self.testLog.informUser("missingMunis", kommun = None)
        print("\nInformera inte om att det saknas för två nyckeltal, vilka år, samt vad som egentligen visas:\n")
        self.testLog.informUser("missingData", "succeededYears")
        print("\nInformera om vilken SEKOMgrupp som visas:\n")
        self.testLog.informUser("sekomCol")
        print("\nInformera om antal kommuner (ser lite lustigt ut nu, sällan det är två nyckeltal på det här sättet)\n")
        self.testLog.informUser("actualQty", "expectedTot")
        print("\nInformera om antal kommuner i snitt (såhär brukar det användas)\n")
        self.testLog.informUser("showSekomAvg")

    def test_reset(self):
        # reset kör bara init igen, inte mycket att testa
        pass

    def test_resetMissingMunis(self):
        self.testLog.addInfo(missingMunis = "Sorsele")
        self.testLog.addInfo(missingMunis = "Övertorneå")
        self.testLog.addInfo(missingMunis = "Kalix")
        self.testLog.addInfo(missingMunis = "Halmstad")
        self.testLog.addInfo(missingMunis = "Flen")
        self.testLog.resetMissingMunis()
        self.assertEqual(len(self.testLog._alertLog["missingMunis"]),0)

if __name__ == '__main__':
    unittest.main()
