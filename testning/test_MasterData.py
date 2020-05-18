import os, sys

sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__))+'/../src/')
path_to_data = os.path.join(os.getcwd(),os.path.dirname(__file__)) + '/../testning/'

import main
import unittest
import json
import API_Anrop as ap




class testDiagrams(unittest.TestCase):
	
		
	def test_nyckeltal(self):
		'''
		Asserts that the MasterData-file includes all the keyvalues that should have been downloaded from Kolada.
		Asserts that every municipality has the correct number of keyvalues compared to the keyvalues that were requested for download.
		'''
		with open(path_to_data + "../data/MasterData.txt", "r") as f:
			mdata = json.load(f)
		myNyckel = ap.NYCKELTAL.split(",")

		for x,y in mdata.items():
			for z in y.keys():
				self.assertIn(z,myNyckel)
			self.assertEqual(len(mdata[x]),len(myNyckel))
	

	def test_ar(self):
		'''
		Checks the MasterData-file for which years and municipalities that the keyvalues contain no data.
		'''
		with open(path_to_data + "../data/MasterData.txt", "r") as f:
			mdata = json.load(f)
		myYear = ap.YEARS.split(",")
		errorFile = open(path_to_data +"./results/test_ar.txt","w",encoding="utf-8")
		errorFile.write("VILKA ÅR SOM SAKNAS FÖR RESPEKTIVE KOMMUN OCH NYCKELTAL"+"\n\n\n")
		errorFile.write("KOMMUN" +"\t"+"|" +"\t" +"NYCKELTAL"+ "\t" +"|" + "\t" +"ÅR"+"\n\n")
		myError = []
		lstError = ""

		for x,y in mdata.items():
			for i, k in y.items():
				try:
					self.assertEqual(len(y[i]),len(myYear))
				except AssertionError:
					for j in myYear:
						if j not in k:
							myError.append(j)
					for n in range(0,len(myError)):
						if n >= (len(myError)-1):
							lstError += myError[n]	
						else:
							lstError += myError[n] +", "
					errorFile.write(str(x) + "\t\t" + str(i) + "\t\t"+ lstError +"\n")
					myError = []
					lstError = ""
			errorFile.write("\n")

		errorFile.close()
	
	def test_data(self):
		'''
		A granular look at what exactly that is missig from each municipality, keyvalue and year.
		'''
		with open(path_to_data + "../data/MasterData.txt", "r") as f:
			mdata = json.load(f)
		
		errorFile = open(path_to_data + "./results/test_data.txt","w",encoding="utf-8")
		errorFile.write("VILKA NYCKELTAL SAMT ÅR OCH KOMMUN SOM SAKNAR DATA OCH VAD SOM SAKNAS"+"\n\n\n")
		errorFile.write("KOMMUN" +"\t"+"|" +"\t" +"NYCKELTAL"+ "\t" +"|" + "\t" +"ÅR"+ "\t" +"|" + "\t" + "VAD SAKNAS"+"\n\n")
		myError = []
		lstError = ""

		for x,y in mdata.items():
			for i, k in y.items():
				for l,m in k.items():
					if None in m.values():
						for v in m.keys():
							if m[v]==None:
								myError.append(v)
										
						for n in range(0,len(myError)):
							if n >= (len(myError)-1):
								lstError += myError[n]	
							else:
								lstError += myError[n] +", "
						errorFile.write(str(x) + "\t\t" + str(i) + "\t\t"+ str(l)+ "\t\t"+ lstError +"\n")
						myError = []
						lstError = ""
			errorFile.write("\n")

		errorFile.close()
		print("\n\nEVEN IF ALL THE TESTS PASSED THERE MIGHT BE ISSUES. MAKE SURE TO REVIEW THE .TXT-FILES IN THE RESULTS FOLDER!\n\n")
		

if __name__ == '__main__':
    unittest.main()