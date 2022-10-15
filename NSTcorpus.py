# -*- coding: utf-8 -*-
"""
NSTcorpus: functions to read the NST corpus, i.e. transcripts and wavfiles

(C) Nadja Althaus 2022
"""
import os, re, subprocess


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




def read_corpus_raw(topdirlist):
    """
            read corpus, transcript by transcript, from nested NST file structure


            Parameters
            ----------
            topdirlist: list of str - directories that are going to be searched for wav and transcript files

            Returns
            ----------
            NSTwavfilenames: list of full paths to wav file names in directories given in topdirlist
            NSTtranscripts: list of full paths to transcript (txt) files, length is same as NSTwavfilenames
            NSTregionofyouth: for each item in wavfilenames/NSTtranscripts, indicate the region of youth of the speaker

         """


# build the directory structure

    NSTwavfilenames = []
    NSTtranscripts = []
    NSTregionofyouth = []
    wavfnames = []

    # for dirName, subdirList, fileList in os.walk(topdir):
    for topdir in topdirlist:
        print(topdir)

        # read the directory tree starting at topdir, make a list of all wavfiles found
        # only use the converted ones which end in _julius
        for dirName, subdirList, fileList in os.walk(topdir):

            for name in fileList:
                #if name.lower().endswith('_julius.wav'):
                if name.lower().endswith('.wav'):

                    # print(os.path.join(dirName,name))
                    wavfnames.append(os.path.join(dirName, name))

        # variables prefixed with NST all share the same order/index/length
        # NSTwavfilenames=wavfnames  #not yet!
        print(str(len(wavfnames)) + ' wavfiles in corpus')

    # walk through all wavfilenames and find corresponding region of youth of speaker
    # and corresponding transcripts, collected in NSTregionofyouth and NSTtranscripts
    counter = 0  # only needed for informative stdout
    print('parse...')
    for wfn in wavfnames:

        if counter % 5000 == 0:
            print(counter)
        wfnparts = re.search('(.+)/speech/(.+)/(.+)\.wav$', wfn)
        wfnprefix = wfnparts.group(1)
        wfnsuffix = wfnparts.group(2)
        wfname = wfnparts.group(3)
        splname = wfnprefix + '/data/' + wfnsuffix + '.spl'
        splcontent = []
        try:

            with open(splname, 'r', encoding='UTF-8') as f:
                splcontent = f.readlines()
        except (FileNotFoundError, IOError):
            print(wfn)
            print("Wrong file or file path: " + splname)
            continue
        NSTwavfilenames.append(wfn)  # only append this if audio actually found
        info_states_start = 0
        record_states_start = 0
        region_of_youth_idx = 0
        transcript_idx = 0
        i = 0
        for l in splcontent:
            if info_states_start > 0 and record_states_start > 0 and region_of_youth_idx > 0 and transcript_idx > 0:
                break
            if re.search('\[Info states\]', l):
                info_states_start = i
                i = i + 1
            elif re.search('\[Record states\]', l):
                record_states_start = i
                i = i + 1
            elif re.search('Region of Youth', l):
                region_of_youth_idx = i
                i = i + 1
            elif re.search(wfname + '.wav', l):
                transcript_idx = i
                i = i + 1
            elif re.search('\[Validation states\]', l):
                break
            else:

                i = i + 1
        counter = counter + 1

        royr = re.search('Region of Youth>-<(.+)>', splcontent[region_of_youth_idx])

        NSTregionofyouth.append(royr.group(1))

        transcriptr = re.search('>-<>-<(.*)>-<[0-9]+>-<[0-9]+>-<' + wfname + '\.wav', splcontent[transcript_idx])
        try:
            NSTtranscripts.append(transcriptr.group(1))
        except AttributeError:
            continue

    print('final number of files used:' + str(len(NSTwavfilenames)))
    return NSTwavfilenames, NSTtranscripts, NSTregionofyouth






def findwav(Types,Transcripts,Wavfiles, type2trans=True):
    """
            create a dictionary type --> wavfiles containing that word (type)


            Parameters
            ----------
               Types: list of str, target words
               Transcripts: list of str, transcripts from NST
               Wavfiles: list of str, wav file names
               type2trans: boolean flag that will trigger construction of a second dictionary if True, type2trans

            Returns
            ----------
            type2wav - a dictionary mapping words to a list of wavfiles containing that word
            type2trans - a dictionary mapping words to a list of transcripts containing that word

         """
    index={}
    for i in range(len(Transcripts)):
        tStripped = strip_punctuation(Transcripts[i])
        tSplit = tStripped.split()
        for s in tSplit:
            index.setdefault(s,[]).append(i)

    type2wav={}
    type2trans={}
    for type in Types:
        for w in index[type]:
            type2wav.setdefault(type,[]).append(Wavfiles[w])
            type2trans.setdefault(type,[]).append(Transcripts[w])
    if not type2trans:
        return type2wav
    else:
        return type2wav, type2trans
