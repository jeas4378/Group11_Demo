# jag lärde mig här: https://www.youtube.com/watch?v=6tNS--WetLI

import unittest
import os, sys

sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__))+'/../src/')
import data_funcs as DF
import InformationLog as IL
from API_Anrop import NYCKELTAL, YEARS

class TestDataFuncs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sort_by_fst_lst(self):
        # några enkla test
        self.assertIsInstance(DF.sort_by_fst_lst([["B","A","C"],[1,2,3.2]]), zip)
        self.assertEqual(list(DF.sort_by_fst_lst([["B","A","C"],[1,2,3.2]],reverse=False)),[("A","B","C"),(2,1,3.2)])
        self.assertEqual(list(DF.sort_by_fst_lst([["B","A","C"],[1,2,3.2]],reverse=True)),[("C","B","A"),(3.2,1,2)])
        self.assertEqual(list(DF.sort_by_fst_lst([[67.3,42.1,98.2],[1,2,3.2],["B","A","C"]],reverse=False)),[(42.1,67.3,98.2),(2,1,3.2),("A","B","C")])

        # ett större exempel med 50 element
        randomWords = ['cope', 'system', 'twist', 'draw', 'call', 'inflation', 'annual',
        'headquarters', 'mislead', 'indoor', 'deep', 'operational', 'ankle',
        'width', 'brother', 'mole', 'index', 'gallery', 'vat', 'realize',
        'pardon', 'dance', 'orthodox', 'grain', 'monk', 'thirsty', 'oh',
        'benefit', 'long', 'rage', 'shoulder', 'immune', 'terminal', 'vain',
        'football', 'result', 'cylinder', 'fare', 'spite', 'beg', 'tidy',
        'dressing', 'colony', 'service', 'growth', 'fastidious', 'earwax',
        'dramatic', 'proper', 'virtue']
        randomNo = [8, 42, 46, 13, 6, 26, 2, 22, 28, 25, 11, 32, 1, 50, 5, 29, 24, 19, 48,
        37, 34, 10, 33, 20, 30, 44, 31, 4, 27, 36, 40, 23, 43, 47, 18, 38, 9, 16, 41, 3,
        45, 14, 7, 39, 21, 17, 15, 12, 35, 49]
        alphabetically = ('ankle','annual','beg','benefit','brother','call','colony',
        'cope','cylinder','dance','deep','dramatic','draw','dressing','earwax','fare',
        'fastidious','football','gallery','grain','growth','headquarters','immune','index',
        'indoor','inflation','long','mislead','mole','monk','oh','operational','orthodox',
        'pardon','proper','rage','realize','result','service','shoulder','spite','system',
        'terminal','thirsty','tidy','twist','vain','vat','virtue','width')
        fifty_no = tuple([i for i in range(1,51)])

        self.assertEqual(list(DF.sort_by_fst_lst([randomWords, randomNo],False)), [alphabetically,fifty_no])

        # ett test som använder "rätt" sorts data - kommuner och siffror
        # OBS : fungerar inte det här *kan* det ligga hos get_all_municipalties
        import random
        kommuner = DF.get_all_municipalties()
        randomPercentages = [random.uniform(0, 100) for i in range(1,291)]
        sortedPercentages = randomPercentages.copy()
        sortedPercentages.sort()
        sortedPercentages = tuple(sortedPercentages)
        self.assertEqual(list(DF.sort_by_fst_lst([randomPercentages,kommuner],reverse = False))[0], sortedPercentages)
        self.assertIn("Sorsele",list(DF.sort_by_fst_lst([randomPercentages,kommuner],reverse = False))[1])

    def test_checkYearsOrder(self):
        self.assertIsNone(DF.checkYearsOrder('2020'))
        # fabricerar YEARS-konstanten från API_Anrop
        YEARS = "2016,2017,2018,2019"
        self.assertEqual(DF.checkYearsOrder('2016', years = YEARS),['2016','2017','2018','2019'])
        self.assertEqual(DF.checkYearsOrder('2017', years = YEARS),['2017','2018','2016','2019'])
        self.assertEqual(DF.checkYearsOrder('2018', years = YEARS),['2018','2019','2017','2016'])
        self.assertEqual(DF.checkYearsOrder('2019', years = YEARS),['2019','2018','2017','2016'])

        YEARS = "2013,2014,2015,2016,2017,2018,2019,2020,2021"
        self.assertEqual(DF.checkYearsOrder('2016', years = YEARS),['2016','2017','2015','2018','2014','2019','2013','2020','2021'])
        self.assertEqual(DF.checkYearsOrder('2019', years = YEARS),['2019','2020','2018','2021','2017','2016','2015','2014','2013'])
        self.assertIsNone(DF.checkYearsOrder('2010', years = YEARS))


    def test_get_data(self):
        # Observera att denna funktion lokalt anropar get_single_data,
        # så om något test misslyckas - kontrollera först denna funktion

        infoLog = IL.InformationLog()
        # Hämta nyckeltalen i NYCKELTAL, åren i YEARS
        keywords = NYCKELTAL.split(',')
        years = YEARS.split(',')
        # returnera alltid 290 kommuner
        for keyword in keywords:
            for year in years:
                self.assertEqual(len(DF.get_data(keyword,year,infoLog)),290)
        # så länge inte året/nyckeltalet är fel
        infoLog.reset()
        with self.assertRaises(ValueError):
            DF.get_data("ABC",year,infoLog)

        infoLog.reset()
        with self.assertRaises(ValueError):
            DF.get_data(keyword,'1900',infoLog)
        # men returnera aldrig en lista med enbart None-värden, vilket är det man får av denna kombo
        infoLog.reset()
        self.assertNotEqual(DF.get_data('N15572','2018',infoLog),[None] * 290)
        self.assertEqual(len(DF.get_data('N15572','2018',infoLog)),290)

    def test_get_single_data(self):
        infoLog = IL.InformationLog()

        # se till att data för Sorsele alltid är None, en int eller en float.
        # skulle kunna utnyttja get_all_municipalties för att loopa över alla kommuner men då
        # blir testerna mer beroende av den funktionen
        keywords = NYCKELTAL.split(',')
        year = '2018'
        for keyword in keywords:
            self.assertTrue(
                (DF.get_single_data(keyword,year,infoLog,kommun='Sorsele') is None)
                or
                isinstance(DF.get_single_data(keyword,year,infoLog,kommun='Sorsele'), int)
                or
                isinstance(DF.get_single_data(keyword,year,infoLog,kommun='Sorsele'), float)
            )
        infoLog.reset()

        # ett test på exakt data jag hämtat från mdata manuellt
        self.assertEqual(DF.get_single_data("N15574",'2017',infoLog,gender='K'),16.3)

        # fel i nyckeltal, år eller kommuner ger ett KeyError
        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.get_single_data("ABC",year,infoLog)

        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.get_single_data(keyword,'1900',infoLog, kommun = "Arjeplog")

        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.get_single_data(keyword,year,infoLog, kommun = "Tyskland")

    def test_calc_sekom_avg(self):
        infoLog = IL.InformationLog()
        # se till att SEKOMsnittet givet Sorsele alltid är None eller en float.
        # skulle kunna utnyttja get_all_municipalties för att loopa över alla kommuner men då
        # blir testerna mer beroende av den funktionen
        keywords = NYCKELTAL.split(',')
        year = '2018'
        for keyword in keywords:
            self.assertTrue(
                (DF.calc_sekom_avg(keyword,year,'Sorsele',infoLog) is None)
                or
                isinstance(DF.calc_sekom_avg(keyword,year,'Sorsele',infoLog),float)
            )

        # fel i nyckeltal, år eller kommuner ger ett KeyError
        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.calc_sekom_avg("ABC",year,'Sorsele',infoLog)

        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.calc_sekom_avg(keyword,'1900','Sorsele',infoLog)

        infoLog.reset()
        with self.assertRaises(KeyError):
            DF.calc_sekom_avg(keyword,year,'Tyskland',infoLog)

        # ett känt värde som det saknas alla kommuners data för
        infoLog.reset()
        self.assertIsNone(DF.calc_sekom_avg('N15572','2018','Sorsele',infoLog))


    def test_get_comparison_list(self):
        infoLog = IL.InformationLog()
        # Obs använder både calc_sekom_avg och get_single_data lokalt, pajjar något kan de
        # behöva ändras
        keywords = NYCKELTAL.split(',')
        years = YEARS.split(',')
        # returnera alltid 3 värden
        for keyword in keywords:
            for year in years:
                self.assertEqual(len(DF.get_comparison_list(keyword,year,'Sorsele',infoLog)),3)

        # skickar vi ett ogiltigt nyckeltal, år eller kommunnamn ska följande ske
        with self.assertRaises(ValueError):
            DF.get_comparison_list("ABC",year,'Sorsele',infoLog)
        with self.assertRaises(ValueError):
            DF.get_comparison_list(keywords[0],year,'Tyskland',infoLog)

        with self.assertRaises(TypeError):
            DF.get_comparison_list(keywords[0],'1900','Sorsele',infoLog)


    def test_get_all_municipalties(self):
        kommuner = DF.get_all_municipalties()
        # Alltid 290 kommuner
        self.assertEqual(len(kommuner),290)
        # Ett urval av kommuner ska finnas
        self.assertIn('Sorsele',kommuner)
        self.assertIn('Arjeplog',kommuner)
        self.assertIn('Malmö',kommuner)
        self.assertIn('Simrishamn',kommuner)
        # ska bara bestå av strängar
        for kommun in kommuner:
            self.assertIsInstance(kommun,str)

        # ska alltid hämtas i samma ordning
        kommuner2 = DF.get_all_municipalties()
        self.assertEqual(kommuner, kommuner2)

    def test_normalize_data(self):
        # tester från exemplet i funktionsbeskrivningen
        l1 = [1,2,None,4]
        l2 = ['a',None,'c','d']
        k1 = ["K1","K2","K3","K4"]
        self.assertEqual(DF.normalize_data(k1,l1,l2),(["K1","K4"],[1,4],['a','d']))
        self.assertEqual(DF.normalize_data(k1,l1),(["K1","K2","K4"],[1,2,4]))

        # tester som anropar andra funktioner borde vi kanske ha men jag
        # har inget smart sätt att generera sånt jag kan verifiera manuellt

    def test_filter_on_SEKOM(self):
        kommuner = DF.get_all_municipalties()
        x_list = [1]*290
        y_list = [2]*290
        # returnera 2 resp. 3 resultatlistor beroende på antal input
        self.assertEqual(len(DF.filter_on_SEKOM('Sorsele',kommuner,x_list)),2)
        self.assertEqual(len(DF.filter_on_SEKOM('Sorsele',kommuner,x_list,y_list)),3)

        # med en kommun ur varje grupp ska det totalt finnas 290 datapunkter
        lila = len(DF.filter_on_SEKOM('Ale', kommuner, x_list)[0])
        gron = len(DF.filter_on_SEKOM('Aneby', kommuner, x_list)[0])
        orange = len(DF.filter_on_SEKOM('Alvesta', kommuner, x_list)[0])
        gul = len(DF.filter_on_SEKOM('Arvika', kommuner, x_list)[0])
        bla = len(DF.filter_on_SEKOM('Avesta', kommuner, x_list)[0])
        self.assertEqual(lila+gron+orange+gul+bla,290)

    def test_move_to_last(self):
        kommuner = DF.get_all_municipalties()
        x_list = [1]*290
        y_list = [2]*290
        # returnera 2 resp. 3 resultatlistor beroende på antal input
        self.assertEqual(len(DF.move_to_last('Sorsele',kommuner,x_list)),2)
        self.assertEqual(len(DF.move_to_last('Sorsele',kommuner,x_list,y_list)),3)

        # grundbeteende
        self.assertEqual(DF.move_to_last('B',['B','C','A','F'],[1,2,3,4]),(['C','A','F','B'],[2,3,4,1]))
        self.assertEqual(DF.move_to_last('F',['B','C','A','F'],[1,2,3,4]),(['B','C','A','F'],[1,2,3,4]))
        self.assertEqual(DF.move_to_last('A',['B','C','A','F'],[1,2,3,4]),(['B','C','F','A'],[1,2,4,3]))

        self.assertEqual(DF.move_to_last('B',['B','C','A','F'],[1,2,3,4],[11,22,33,44]),
                                            (['C','A','F','B'],[2,3,4,1],[22,33,44,11]))
        self.assertEqual(DF.move_to_last('F',['B','C','A','F'],[1,2,3,4],[11,22,33,44]),
                                            (['B','C','A','F'],[1,2,3,4],[11,22,33,44]))
        self.assertEqual(DF.move_to_last('A',['B','C','A','F'],[1,2,3,4],[11,22,33,44]),
                                            (['B','C','F','A'],[1,2,4,3],[11,22,44,33]))

        # fel om vi försöker flytta något som inte finns
        with self.assertRaises(ValueError):
            DF.move_to_last('Tyskland',kommuner,x_list)

    def test_create_list_of_colors(self):
        # grundbeteende
        infoLog = IL.InformationLog()
        self.assertEqual(DF.create_list_of_colors(["A","B","C"],infoLog,'blue','red',"B"),['blue','red','blue'])
        self.assertEqual(DF.create_list_of_colors(["A","B","C"],infoLog,'blue','red',"X"),['blue','blue','blue'])
        self.assertEqual(DF.create_list_of_colors([],infoLog,'blue','red',"X"),[])

        #returnera alltid en lika lång lista som den får
        import random
        length = random.randint(1,300)
        self.assertEqual(len(DF.create_list_of_colors(["A"]*length,infoLog,'blue','red',"X")),length)

    def test_no_per_sekom(self):
        # med en kommun ur varje grupp ska det totalt finnas 290 datapunkter
        lila = DF.no_per_sekom('Ale')
        gron = DF.no_per_sekom('Aneby')
        orange = DF.no_per_sekom('Alvesta')
        gul = DF.no_per_sekom('Arvika')
        bla = DF.no_per_sekom('Avesta')
        self.assertEqual(lila+gron+orange+gul+bla,290)

        # fel om en kommunen ej existerar
        with self.assertRaises(KeyError):
            DF.no_per_sekom('Tyskland')
    
    def test_round_values(self):

        lst1 = [0.60,21.3,34.9]
        lst2 = [15.2,28.7,32.1]
        lst3 = [11.1,256.43,9.07]

        self.assertEqual(DF.round_values(lst1),(1,21,35))
        self.assertEqual(DF.round_values(lst1,lst2),([1,21,35],[15,29,32]))
        self.assertEqual(DF.round_values(lst1,lst2,lst3),([1,21,35],[15,29,32],[11,256,9]))

if __name__ == '__main__':
    unittest.main()
