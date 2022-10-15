#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NSTlexicon: functions to read the NST lexicon and obtain token/base form counts for a corpus of text
(C) Nadja Althaus 2022
"""


import re
from collections import Counter
import profile


######################
#
# AUX FUNCTIONS
#
######################

from string import punctuation
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

######################
#
# CORE FUNCTIONS
#
######################



def read_lexicon(lexfile='swe030224NST.csv', maxentries=0):
    """
            Reads the NST lexicon from input csv file

            Parameters
            ----------
            lexfile : csv file name (NST lexicon)

            maxentries : max number of items read from the top of the file,
                        is ignored if 0

            Returns
            ----------
            Lemma (list of str): lexical entries, includes morphological forms as separate entries
            PosDict (dict, key: str, val: str or list): keys: Lemma, values: corresponding part of speech tag or list, e.g. 'NN', or ['NN','VB']
            MorphDict (dict, key: str, val: str or list): keys: Lemma, values: morphological tags
            PhonDict (dict, key: str, val: str) keys: Lemma, values: phonological transcript
            NumSyllDict (dict, key: str, val: int): keys: Lemma, values number of syllables
            SyllDict (dict, key: str, val: list of str): keys: Lemma, values: list of syllable transcripts, e.g. ['""A:', 'pa'] for 'apa'
            AccentDict(dict, key: str, val: list of int): keys: Lemma, values: list of int with one value per syllable (unstressed = 0), e.g. disyllabic Accent 2 is [2,0], disyllabic Accent 1 is [1,0]
            DecompDict(dict, key: str, val: str):keys: Lemma, values: str indicating morphological decomposition, morpheme boundaries indicated with '+', e.g. sjukhus -> 'sjuk+hus'
            BaseDict (dict, key: str, val: str):keys: Lemma, values: base lexical entry, e.g. apan -> apa
            SemDict (dict, key: str, val: int):keys: Lemma, values: semantic ID code
        """
    
    #returns Lemma, PosDict, MorphDict, PhonDict, NumSyllDict, SyllDict, AccentDict, DecompDict, BaseDict, SemDict


    print('reading lex')
    Lemma=[]
    pos=[]
    morph=[]
    decomp=[]
    transcript=[]
    num_syll=[]
    syllables=[]
    accent=[]
    #base=[]
    PosDict=dict()
    MorphDict=dict()
    PhonDict=dict()
    NumSyllDict=dict()
    SyllDict=dict()
    AccentDict=dict()
    DecompDict=dict()
    BaseDict=dict()
    SemDict=dict()
    
    
    with open(lexfile, 'r', encoding='ISO-8859-1') as f:
        counter=1
        for line in f:
            if counter%100000==0:
                print(counter)
            if maxentries>0 and counter> maxentries:
                return Lemma, PosDict, MorphDict, PhonDict, NumSyllDict, SyllDict, AccentDict, DecompDict, BaseDict, SemDict
                break
                    
            cells=re.split(';', line)

         
            Lemma.append(cells[0])

            pos.append(cells[1])
            morph.append(cells[2])
            decomp.append(cells[3])
            transcript.append(cells[11])
            
            #count the number of syllables
            numsyll=cells[11].count('$')+1
            num_syll.append(numsyll)
            
            #create a list of syllables
            if numsyll>1:
                syllables.append(re.split('\$',cells[11]))
            else:
                syllables.append(cells[11])
              
            thisaccent=[]
            
            #parse accent info
            for syll in re.split('\$', cells[11]):
                
                acc2r=re.match('""',syll)
                
                if not acc2r:
                    acc1r=re.match('"', syll)
                    if acc1r:
                        thisaccent.append(1)
                    else:
                        thisaccent.append(0)
                else:
                    thisaccent.append(2)
            
            accent.append(thisaccent)
            
            #handle cases like avskyA avskyB

            base_r=re.search('^([a-zA-ZåäöÅÄÖ]*)[AB]+\|', cells[32])
            if not base_r:
                base_r=re.search('^([a-zA-ZåäöÅÄÖ]*)\|',cells[32])
            
            
            
            if not base_r:
                    thisbase=cells[0]
            else:
                
                thisbase=base_r.group(1)
            
            

           
            #extract semantic ID information, a numeric tag. 
            #not all entries in the NST lexicon have this
            sem_r=re.search('^[a-zA-ZåäöÅÄÖ]*\|([0-9]*)',cells[32])
            if sem_r:
                if not cells[0] in SemDict:
                    SemDict[cells[0]]=sem_r.group(1)
                else:
                    thissem=SemDict[cells[0]]
                    if not isinstance(thissem, list):
                        thissem = [thissem]
                    if not sem_r.group(1) in thissem:
                        thissem.append(sem_r.group(1))
                    SemDict[cells[0]]=thissem
       

            else:
                thislemma=cells[0]

                if not cells[0] in SemDict:
                    SemDict[cells[0]]=''
            
            
            if not cells[0] in PosDict:
                PosDict[cells[0]]=cells[1]
            else:
                if type(PosDict[cells[0]]) is list:
                    if not cells[1] in PosDict[cells[0]]:
                        PosDict[cells[0]].append(cells[1])
                else:
                    if not PosDict[cells[0]]==cells[1]:
                        previouspos=PosDict[cells[0]]
                        PosDict[cells[0]]=list()
                        PosDict[cells[0]].append(previouspos)
                        PosDict[cells[0]].append(cells[1])
                
            if not cells[0] in MorphDict:
                MorphDict[cells[0]]=cells[2]
            else:
                if type(MorphDict[cells[0]]) is list:
                    if not cells[2] in MorphDict[cells[0]]:
                        MorphDict[cells[0]].append(cells[2])
                else:
                    if not MorphDict[cells[0]]==cells[2]:
                        previous=MorphDict[cells[0]]
                        MorphDict[cells[0]]=list()
                        MorphDict[cells[0]].append(previous)
                        MorphDict[cells[0]].append(cells[2])
              
            if not cells[0] in PhonDict:
                PhonDict[cells[0]]=cells[11]
            else:
                if type(PhonDict[cells[0]]) is list:
                    if not cells[11] in PhonDict[cells[0]]:
                        PhonDict[cells[0]].append(cells[11])
                else:
                    if not PhonDict[cells[0]]==cells[11]:
                        previousphon=PhonDict[cells[0]]
                        PhonDict[cells[0]]=list()
                        PhonDict[cells[0]].append(previousphon)
                        PhonDict[cells[0]].append(cells[11])
                    
                
            if not cells[0] in NumSyllDict:
                NumSyllDict[cells[0]]=cells[11].count('$')+1
            
            if not cells[0] in SyllDict:
                SyllDict[cells[0]]=re.split('\$', cells[11])
            else:
                if type(SyllDict[cells[0]][0]) is list:
                    if not re.split('\$',cells[11]) in SyllDict[cells[0]]:
                        SyllDict[cells[0]].append(re.split('\$', cells[11]))
                else:
                    if not SyllDict[cells[0]]==re.split('\$', cells[11]):
                        previoussyll=SyllDict[cells[0]]
                        SyllDict[cells[0]]=list()
                        SyllDict[cells[0]].append(previoussyll)
                        SyllDict[cells[0]].append(re.split('\$', cells[11]))
                        
            
            if not cells[0] in AccentDict:
                AccentDict[cells[0]]=thisaccent
               
                
            else:
                
                if type(AccentDict[cells[0]]) is list:
                    #it could be a simple list, i.e. just one previous record
                    if not type(AccentDict[cells[0]][0]) is list:
                        #just check that it's not identical to the current thisaccent
                        
                        if not AccentDict[cells[0]]==thisaccent:
                            #now make a list
                            previousacc=AccentDict[cells[0]]
                            AccentDict[cells[0]]=list()
                            AccentDict[cells[0]].append(previousacc)
                            AccentDict[cells[0]].append(thisaccent)
                    else:
                        #we already have at least 2 previous accents
                        #check that the current one is different from those previous ones
                        if not thisaccent in AccentDict[cells[0]]:
                            AccentDict[cells[0]].append(thisaccent)
                            
                
            if not cells[0] in DecompDict:
                DecompDict[cells[0]]=cells[3]
            
            
            if not cells[0] in BaseDict:
                BaseDict[cells[0]]=thisbase
            else:
                if type(BaseDict[cells[0]]) is list:
                    if not thisbase in BaseDict[cells[0]]:
                        BaseDict[cells[0]].append(thisbase)
                else:
                    if not BaseDict[cells[0]]==thisbase:
                        prevbase=BaseDict[cells[0]]
                        BaseDict[cells[0]]=list()
                        BaseDict[cells[0]].append(prevbase)
                        BaseDict[cells[0]].append(thisbase)
                
            counter=counter+1
            
            #need to correct a few entries that have been coded erroneously in the DB
            #baseforms: är = vara, var = vara, hade = ha, har = ha, kunde = kunna, kan = kunna, sade = säga,säger säga 
            BaseDict['är']='vara'
            BaseDict['var']='vara'
            BaseDict['har']='ha'
            BaseDict['hade']='ha'
            BaseDict['säger']='säga'
            BaseDict['sade']='säga'
            BaseDict['kan']='kunna'
            BaseDict['kunde']='kunna'
            BaseDict['fick']='få'
            BaseDict['får']='få'
            BaseDict['mår']='må'
            BaseDict['mådde']='må'
            BaseDict['skulle']='skola'
            BaseDict['skall']='skola'
            BaseDict['ska']='skola'
            BaseDict['vill']='vilja'
            BaseDict['ville']='vilja'
            BaseDict['sett']='se'
            PosDict['får']=['VB', 'NN']
            MorphDict['får']='AKT|PRS'
            PosDict['flicka']='NN'#was also tagged as VB, but this doesn't occur in Lexin and seems misleading
            
            
            
            
    return Lemma, PosDict, MorphDict, PhonDict, NumSyllDict, SyllDict, AccentDict, DecompDict, BaseDict, SemDict




def lookUp(word, Lemma, PosDict, MorphDict, PhonDict, NumSyllDict, SyllDict, AccentDict, DecompDict, BaseDict):
    """
            Lexicon lookup for 'word'
            Prints information to std out

            Parameters
            ----------
            Lemma, PosDict, MorphDict, PhonDict, NumSyllDict, SyllDict, AccentDict, DecompDict, BaseDict - outputs from read_lexicon()

            Returns
            ----------
         """
    print('****\nLooking up '+word+':')
    print('POS:\t'+ str(PosDict[word]))
    print('Morph:\t'+ str(MorphDict[word]))
    print('Phon:\t'+ str(PhonDict[word]))
    print('Syllables:\t'+ str(NumSyllDict[word])+'/'+str(SyllDict[word]))
    print('Accent:\t', AccentDict[word])
    print('Decomp:\t', DecompDict[word])
    print('Base:\t', BaseDict[word])
    

            






def TokenFrequencies(Transcripts):
    """
            get token frequency counts for a set of transcripts

            Parameters
            ----------
            Transcripts - list of str: list of sentences, NST transcripts (without <s> tags)

            Returns
            ----------
            TokenFreq: Counter
            indicates number of occurrences of each token in Transcripts
         """
    C = []
    for t in Transcripts:
        tStripped = strip_punctuation(t)
        tSplit = tStripped.split()
        for s in tSplit:
            C.append(s)
    TokenFreq = Counter(C)
    return TokenFreq



def TokenBaseFrequencies(Transcripts, BaseDict):
    """
        Like TokenFrequencies, but with an additional output that counts baseforms, i.e. morphological forms mapped to base
              
        Parameters
        ----------
        Transcripts - list of str: list of sentences
        BaseDict - mapping from token form to base form

        Returns
        ----------
        TokenFreq: Counter
        indicates number of occurrences of each token in Transcripts
     """  
    #transcripts is a list of sentences without <s> tags
    C=[]
    for t in Transcripts:
        tStripped=strip_punctuation(t)
        tSplit=tStripped.split()
        for s in tSplit:
            C.append(s)
    TypeFrequencies=Counter(C)
    CorpusLemmatised=list()

    for w in C:
        if w in BaseDict:
            if type(BaseDict[w]) is str:
                CorpusLemmatised.append(BaseDict[w])
            else:
                CorpusLemmatised.append(BaseDict[w][0])
        else:
            CorpusLemmatised.append(w)

    LemmaFrequencies=Counter(CorpusLemmatised)
    return TypeFrequencies, LemmaFrequencies




 
def BaseFreqAboveZero(Corpus, Lemma, BaseDict):
    """
        Base frequencies, but only for items that occur in Corpus
              
        Parameters
        ----------
        corpus - str: list of sentences
        Lemma - list of possible word forms
        BaseDict - mapping from token form to base form

        Returns
        ----------
        Filtered: dictionary, keys: word, values: counts
     """  
    if type(Corpus) is str:
        TF, LF=frequencies(Corpus,BaseDict)

    elif type(Corpus) is list:
        TF, LF=TokenBaseFrequencies(Corpus,BaseDict)
    Filtered=dict()
    for word in Lemma:
        if LF[word]>0:
            Filtered[word]=LF[word]
    return Filtered

