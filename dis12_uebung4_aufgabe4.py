import os, codecs, re, csv, math
import pandas as pd
from collections import Counter
import numpy as np
import json

def ReadData(pfad,Filelist):
    """
    Files im Zielpfad werden eingelesen.
    Wörter aus allen Files werden normalisiert.
    """
    MainDict = {}
    
    for root, dirs, files in os.walk(pfad):
        for filename in files:
            filedir = root + '/' + filename
            with codecs.open(filedir, 'r', encoding='utf-8') as file: # damit das Zeichen æ in Cæsar gelesen werden kann, muss es mit utf-8 gelsen werden
                
                Filelist.append(filename)

                # dict beinhaltet alle Terme mit der Termfrequency pro Dok.
                tf_dict = CalcTF(Normalize(file),filename)

                # terme mit keys werden aus tf_dict ins MainDict übernommen
                for key in tf_dict:
                    if key in MainDict.keys():
                        MainDict[key].update(tf_dict[key])
                    else:
                        MainDict[key] = tf_dict[key]
    return MainDict 

def Normalize(file):
    """
    input: string
    output: list
    Funktion hat rohe Daten aus txt Datei als Input.
    Satzzeichen und Formatierung werden gelöscht.
    """
    filedata = file.read().splitlines()  # file wird gelesen

    only_sentences = [] 
    clean_sentences = []
    list_of_words = []

    # filtern von sätzen aus data
    for item in filedata:
        if item.startswith('\t', 0, 1):
                only_sentences.append(item)

    # filtern von \t aus sätzen
    for sentence in only_sentences:
        clean_sentence = sentence.replace("\t","")
        clean_sentences.append(clean_sentence)

    # Sätze werden zu Wörter und werden normalisiert. 
    for sentence in clean_sentences:
        words_in_sentence = re.compile(r'\W+', re.UNICODE).split(sentence) # sätze werden gesplitet und satzzeichen entfernt
        for word in words_in_sentence:
            if not word == '': # Leerzeichen werden ignoriert
                list_of_words.append(word.lower())
    return list_of_words 

def CalcTF(listofwords,filename):
    """
    input: list, string
    output: dict
    Mit den normalisierten Wörtern und dem Dateinamen werden die Terme pro Dokument gezählt. 
    """
    dict = {}
    countedwords = Counter(listofwords)
    for word in countedwords:
        list = [countedwords[word]]
        dict[word] = {filename : list}
    return dict

def CalcTFIDF(dict):
    """
    input: dict
    output: dict
    Berechnet auf Grundlage der Termfrequency einzelner Terme den tf-idf Wert jedes Term für jedes Dok. 
    """
    for term in dict.keys():
        df = len(dict[term].keys())
        for filename in dict[term].keys():
            tf = sum(dict[term][filename])
            tfidf = round(1 + math.log10(tf) * math.log10(37/df),2) # kleiner cheat an der Stelle, weil ich weiß, dass es 37 Dokumente sind :p
            dict[term][filename].append(tfidf)

    return dict

def CalcVektor(dict,filelist):
    """
    input: dict
    output: dict
    Berechnet die Vektorlängen jedes Dokuments.
    """
    # for filename in filelist:
    
    for filename in filelist: 
        counter = 0
        vektorl = 0
        for term in dict.keys():
            if filename in dict[term].keys():
                counter += dict[term][filename][0]**2

        vektorl = math.sqrt(counter)

        for term in dict.keys():
            if filename in dict[term].keys():
                nomal = round((dict[term][filename][0]/vektorl),2)
                dict[term][filename].append(nomal)
    return dict

def UserInput():
    eingabe = input("Bitte geben Sie nur klein geschriebene Wörter ohne Satzzeichen ein:\n")
    return eingabe

def CheckInput(string,vektor_dict):
    list = string.split()
    counted_list = Counter(list)
    return counted_list

def CalcInput(Input):
    calc = 0
    # berechnung der Vektorlänge der Eingabe
    for word in Input:
        calc += Input[word]**2
    vektor_len = math.sqrt(calc)

    # berechnung der normalisierunge pro Term
    dict = {}
    for word in Input:
        dict[word] = round((Input[word]/vektor_len),2)
    return dict

def CalcKosinus(input, term_dict, filelist):
    input_dict = CalcInput(input) 
    # berechnung des kosinus pro Dokument
    kosinus_dict = {}
    for filename in filelist: 
        calc = 0
        kosinus = 0
        for term in input_dict.keys():
            try:
                calc = (term_dict[term][filename][2] * input_dict[term])
            except:
                pass
            kosinus += calc     
        kosinus_dict[filename] = kosinus       
    return kosinus_dict

def TopHits(dict):
    c = Counter(dict)
    mc = c.most_common(3)
    output = print("\nTop 3 Hits für Ihre Anfrage lauten:\n",
    mc[0],"\n",
    mc[1],"\n",
    mc[2])
    return output

def Main():
    filelist = [] # Liste aller Filenames
    tfidf_dict = CalcTFIDF(ReadData(".\Shakespeare",filelist))#-> Listewerte pro File = [tf, tfidf]
    vektor_dict = CalcVektor(tfidf_dict,filelist) #-> Listewerte pro File = [tf, tfidf, normal. Vektor]
    Input = CheckInput(UserInput(),vektor_dict)
    TopHits(CalcKosinus(Input, vektor_dict,filelist))

    exit = input('\nEnter zum beenden...')
    return
    
Main()