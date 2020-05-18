import os, sys

sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__))+'/../src/')
path_to_data = os.path.join(os.getcwd(),os.path.dirname(__file__)) + '/../testning/'

import main
import unittest
import diagram_classes
import json
from data_funcs import *
from InformationLog import *



class testDiagrams(unittest.TestCase):


	def test_diagram1_dropdowns(self):
		'''
		Ensure that all combination of keyvalues and years produces a complete set containing data for all municipalities
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = diagrams._1_keywords
		errorFile = open(path_to_data + "./results/diagram1_dropdowns.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 1\n\n\n")
		errorFile.write("VILKA ÅR SOM SAKNAS FÖR RESPEKTIVE KOMMUN OCH NYCKELTAL"+"\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()

		for key in keyword:
			for y in year:
				m = get_data(key,y,infoLog,gender = "M")
				f = get_data(key,y,infoLog,gender = "K")
				for i in range(0,len(m)):
					try:
						self.assertNotEqual(None,m[i])
						self.assertNotEqual(None,f[i])
						self.assertNotEqual(0.0,m[i])
						self.assertNotEqual(0.0,f[i])
						self.assertNotEqual("",m[i])
						self.assertNotEqual("",f[i])
					except AssertionError:
						errorFile.write("Nyckeltal "+str(key)+", "+str(y)+", " + str(mun[i])+ ".\n")
				errorFile.write("\n")
			errorFile.write("\n")
		errorFile.close()
	
	def test_diagram1_sekom(self):

		'''
		Checks wether all the municipalities in a SEKOM-group contains data. If not, it will write how many municipalities it found data for in that group. 
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = diagrams._1_keywords
		errorFile = open(path_to_data + "./results/diagram1_sekom.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 1 SEKOM\n\n\n")
		infoLog = InformationLog()
		sekom = {'Avesta':['Blå',59], 'Boden':['Grön',65], 'Hudiksvall':['Gul',75], 'Kungsbacka':['Lila',36], 'Falun':['Orange',55]}
		mun = get_all_municipalties()

		for key in keyword:
			for y in year:
				m = get_data(key,y,infoLog,gender = "M")
				f = get_data(key,y,infoLog,gender = "K")
				mun2, m2, f2 = normalize_data(mun,m,f)
				for kommun, data in sekom.items():
					mun3, m3, f3 = filter_on_SEKOM(kommun,mun2,m2,f2)
					try:
						self.assertEqual(len(mun3), data[1])
					except AssertionError:
						errorFile.write("Nyckeltal "+str(key)+", "+str(y)+", SEKOM-grupp " +str(data[0]) + ", " + str(len(mun3)) +" av "+ str(data[1]) + " kommuner.\n")
			errorFile.write("\n")
		errorFile.close()


	def test_diagram2_dropdowns(self):

		'''
		Checks wether there is data for all municipalities for all years for the keyvalue N15820. Municipalities that are missing data
		will be written to the error file.
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		errorFile = open(path_to_data + "./results/diagram2_dropdowns.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 2\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()

		
		for y in year:
			col = get_data("N15820",y,infoLog)
			for x in range(0,len(col)):
				try:
					self.assertNotEqual(None,col[x])
					self.assertNotEqual("",col[x])
					self.assertNotEqual(0.0,col[x])
				except AssertionError:
					errorFile.write("Nyckeltal N15820"+", "+str(y)+", " + str(mun[x])+ ".\n")
			errorFile.write("\n")
		errorFile.close()
	
	def test_diagram2_sekom(self):

		'''
		Checks wether all the municipalities in a SEKOM-group contains data. If not, it will write how many municipalities it found data for in that group. 
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = diagrams._1_keywords
		errorFile = open(path_to_data + "./results/diagram2_sekom.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 2 SEKOM\n\n\n")
		infoLog = InformationLog()
		sekom = {'Avesta':['Blå',59], 'Boden':['Grön',65], 'Hudiksvall':['Gul',75], 'Kungsbacka':['Lila',36], 'Falun':['Orange',55]}
		mun = get_all_municipalties()

		for key in keyword:
			for y in year:
				var = get_data(key,y,infoLog)
				ed = get_data("N15820",y,infoLog)
				mun2, ed2, var2 = normalize_data(mun,ed,var)
				for kommun, data in sekom.items():
					mun3, ed3, var3 = filter_on_SEKOM(kommun,mun2,ed2,var2)
					try:
						self.assertEqual(len(mun3), data[1])
					except AssertionError:
						errorFile.write("Nyckeltal "+str(key)+", "+str(y)+", SEKOM-grupp " +str(data[0]) + ", " + str(len(mun3)) +" av "+ str(data[1]) + " kommuner.\n")
			errorFile.write("\n")
		errorFile.close()


	def test_diagram3_over(self):

		'''
		Checks which municipalities that are missing data for the keyvalues portraying data for results over the national test and writes the
		missings ones to file.
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = {'Engelska': ['N15574','N15573'], 'Matematik':['N15572','N15571'], 'Svenska':['N15570','N15569']}
		errorFile = open(path_to_data + "./results/diagram3_over.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 3\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()


		for key in keyword:
			for y in year:
				for kommun in mun:
					data_over = get_comparison_list(keyword[key][0], y, kommun, infoLog)
					try:
						self.assertFalse(None in data_over)
					except AssertionError:
						errorFile.write(str(key)+ ", " + str(y)+ ", " +str(kommun) + "\n")
				errorFile.write("\n")
		errorFile.close()

	def test_diagram3_under(self):

		'''
		Checks which municipalities that are missing data for the keyvalues portraying data for results under the national test and writes the
		missings ones to file.
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = {'Engelska': ['N15574','N15573'], 'Matematik':['N15572','N15571'], 'Svenska':['N15570','N15569']}
		errorFile = open(path_to_data + "./results/diagram3_under.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 3\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()


		for key in keyword:
			for y in year:
				for kommun in mun:
					data_under = get_comparison_list(keyword[key][1], y, kommun, infoLog)
					try:
						self.assertFalse(None in data_under)
					except AssertionError:
						errorFile.write(str(key)+ ", " + str(y)+ ", " +str(kommun)  + "\n")
				errorFile.write("\n")
		errorFile.close()

	
	def test_diagram4_dropdown(self):

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = {'Engelska': ['N15574','N15573'], 'Matematik':['N15572','N15571'], 'Svenska':['N15570','N15569']}
		errorFile = open(path_to_data + "./results/diagram4_dropdown.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 4\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()


		for v,w in keyword.items():
			for key in w:
				for y in year:
					data = get_data(key,y,infoLog)
					mun2, data2 = normalize_data(mun, data)
					try:
						self.assertEqual(len(mun2), 290)
					except AssertionError:
						if key == keyword[v][0]:
							errorFile.write(str(v)+ ", över NP, " +str(key)+ ", " + str(y)+ ", "  + str(len(mun2))+ " av 290.\n")
						else:
							errorFile.write(str(v)+ ", under NP, " +str(key)+ ", " + str(y)+ ", "  + str(len(mun2))+ " av 290.\n")
				errorFile.write("\n")
		errorFile.close()

	
	def test_diagram4_data(self):
		'''
		Checks wether all municipalities has data for all years and keyvalues. If they don't it will be written to an error-file.
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		keyword = {'Engelska': ['N15574','N15573'], 'Matematik':['N15572','N15571'], 'Svenska':['N15570','N15569']}
		errorFile = open(path_to_data + "./results/diagram4_data.txt","w",encoding="utf-8")
		errorFile.write("DIAGRAM 4\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()


		for v,w in keyword.items():
			for key in w:
				for y in year:
					data = get_data(key,y,infoLog)
					for x in range(0,len(data)):
						try:
							self.assertNotEqual(None,data[x])
							self.assertNotEqual("",data[x])
							self.assertNotEqual(0.0,data[x])
						except AssertionError:
							if key == keyword[v][0]:
								errorFile.write(str(v)+ ", över NP, " +str(key)+ ", " + str(y)+ ", "  + str(mun[x])+ ".\n")
							else:
								errorFile.write(str(v)+ ", under NP, " +str(key)+ ", " + str(y)+ ", "  + str(mun[x])+ ".\n")
					errorFile.write("\n")
				errorFile.write("\n")
		errorFile.close()
	
	def test_diagram5_data(self):

		'''
		Checks wether all municipalities has data for all years and keyvalues. If they don't they get written to an error-file.
		'''

		diagrams = main.interactive_diagrams()
		year = diagrams._years
		errorFile = open(path_to_data + "./results/diagram5_data.txt","w",encoding="utf-8")
		errorFile.write("VILKA ÅR SOM SAKNAS FÖR RESPEKTIVE KOMMUN OCH NYCKELTAL"+"\n\n\n")
		infoLog = InformationLog()
		mun = get_all_municipalties()
		keyword = diagrams._1_keywords


		for key in keyword:
			for y in year:
				for kommun in mun:
					data = get_comparison_list(key, y, kommun, infoLog)
					try:
						self.assertNotEqual(None,data[0])
						self.assertNotEqual("",data[0])
						self.assertNotEqual(0.0, data[0])
					except AssertionError:
						errorFile.write(str(key)+", " + str(y)+", " + str(kommun)+"\n" )
			errorFile.write("\n")
		errorFile.close()
		print("\n\nEVEN IF ALL THE TESTS PASSED THERE MIGHT BE ISSUES. MAKE SURE TO REVIEW THE .TXT-FILES IN THE RESULTS FOLDER!\n\n")
		

if __name__ == '__main__':
    unittest.main()