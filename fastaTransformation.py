import pandas as pd
from Bio import SeqIO


#Setting up excel file format: columns of interest, either based on name or index (we use the most stable property of each)

barcodeCol = 0
virNameCol = "fastaFile header"
excelSheet = pd.read_excel('path/to/the/file.xlsx') #specific table extracted using Pandas library

#transforming the data into the required structures
excelDict = excelSheet.to_dict()
fastaFile = 'tmpFasta.fasta' 
records_list = list(SeqIO.parse(fastaFile, "fasta")) #loads the fasta file as a list of dictionary, each dictionary storing data from a sequence


def checker(dictio, val):
    for ind,value in dictio.items():
        if val == value:
            return ind
        else:
            continue
    return None

#we look for the barcode in each id element of each sequence, then we check if we find a match in the excel file (structured as a dictionary) 
regex = r"barcode[0-9][0-9]"
for i in range(len(records_list)): 
    checkedIndex = checker(excelDict[barcodeCol], re.findall(regex, records_list[i].id)[0][7:9]) 
    if checkedIndex is not None: #if we find a match then we update the fasta data using the index that matched and the right column name to get the data (similar to a vertical lookup)
        records_list[i].id = excelDict[virNameCol][checkedIndex]
        records_list[i].name = excelDict[virNameCol][checkedIndex]
        records_list[i].description = excelDict[virNameCol][checkedIndex]
    else:
        continue

#once we updated the fasta file we can save it with a specific name to imply the change
fastaFile = input_file['metadata']['name']
fileName = fastaFile.replace('.fasta', '') + 'GISAID' + '.fasta'
SeqIO.write(records_list, "*PATH*\\output\\"+fileName, "fasta")
