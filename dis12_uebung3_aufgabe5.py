import os, codecs, re, csv
from collections import Counter

def DataCleaner(data):
    only_sentences = []
    clean_sentences = []
    ListOfWords = []

    # filtern von sätzen aus quelle
    for item in data:
        if item.startswith('\t', 0, 1):
                only_sentences.append(item)
    
    # filtern von \t aus sätzen
    for item in only_sentences:
        clean_item = item.replace("\t","")
        clean_sentences.append(clean_item)

    # aufsplitten von sätzen in wörter
    for item in clean_sentences:
        words_in_item = item.split(' ')
        for word in words_in_item:
            ListOfWords.append(word.lower())

    # sonderzeichen raus filtern
    # funtioniert noch nicht ganz
    bad_chars = ['.', '!', '?', ',', ',-', ';']
    check = re.compile(r'\.|\!|\?|\,|\,-|\;')
    for item in ListOfWords:
        if check.search(item):
            for char in bad_chars:
                if char in item:
                    item.replace(char, '')

    return ListOfWords #list

def ExportToCSV(dict):
    with open('shakespear_wordcount.csv', 'w') as f:
        for key in dict.keys():
            f.write("%s;%s\n"%(key, dict[key]))

    return

def main(pfad):
    GlobalList = []

    for root, dirs, files in os.walk(pfad):
        for filename in files:
            filedir = root + '/' + filename
            with codecs.open(filedir, 'r', encoding='utf-8') as f: # damit das Zeichen æ in Cæsar gelesen werden kann, muss es mit utf-8 gelsen werden
                filedata = f.read().splitlines()
                for item in DataCleaner(filedata):
                    GlobalList.append(item)

    # umwandlung von collections.counter in ein dict
    csv_dict = dict(Counter(GlobalList))
    
    # export nach csv
    ExportToCSV(csv_dict)

main(".\Shakespeare")