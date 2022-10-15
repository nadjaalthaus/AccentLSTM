# -*- coding: utf-8 -*-

"""
NSTjulius: functions to use Julius speech recognizer and handle the output

(C) Nadja Althaus 2022
"""


import re
import subprocess
import os
import numpy as np





def run_julius(wavlistfile):
    """
    Calls julius via the command line and processes the input wavfiles to perform speech recognition (using the precompiled Swedish language model).
    Results are going to be stored in text files with same name as wav input file + suffix .out

    __________
    Parameters:
        wavlistfile: the name of a textfile that lists wav files to be processed, one per line


    """
    print('run julius')
    #wavlistfile is a list of wavfiles, one per line
    juliuscall=['julius', '-C', 'julius.jconf', '-nosectioncheck', '-hlist', 'tied.lis', '-input', 'file', '-d', 'NSTbingram']
    juliuscall.append('-v')
    juliuscall.append('juliusdict1.txt')
    juliuscall.append('-h')
    juliuscall.append('tied_32_2.mmf')
    juliuscall.append('-walign')
    juliuscall.append('-1pass')
    juliuscall.append('-filelist')
    juliuscall.append(wavlistfile)
    juliuscall.append('-outfile')
    print('start subprocess')
    subprocess.call(juliuscall)
    #results are going to be in text files with same name as wav input file + .out

def parse_julius_output(BaseDict, jfile):
    """
        Processes julius output
        __________
        Parameters:
            BaseDict: dictionary mapping each word form to the corresponding base
                        (e.g. both 'bil' (car) and 'bilar' (cars) map to 'bil')
            jfile: a julius output file
        __________
        Returns:

            Parse: a dictionary mapping the index of each word to a list containing
                - base (e.g. 'bil')
                - start timestamp
                - end timestamp
                - actual recognised form (e.g. 'bilar')
                - parse_score
            WIndex: a dictionary mapping all base forms of words recognised in the parsed file to their index
                    e.g. if the 3rd recognised word was 'bilar' (cars), then WIndex['bil'] will be 3.



        """

    Parse=dict()
    WIndex=dict()
    align_start=False
    align_start_line=0
    align_end_line=0
    jout=''

    with open(jfile, 'r', encoding='utf-8') as f:
        i=0
        Lines=[]
        for l in f:

            #if wavname in l:
            #    fn_found=True

            if '=== begin forced alignment ===' in l:

                align_start_line=i+4
            if '=== end forced alignment ===' in l:
                align_end_line=i-1
            Lines.append(l)
            i=i+1
        if align_start_line==0 or align_end_line==0:
            #something is wrong
            print('Beginning or end not found')
            return Parse
        #skip the header lines of alignment
        #read a formatted string:

        RecogList=Lines[align_start_line:align_end_line]

        p_idx=0
        for l in RecogList:

            p=re.search(r'\[\s*([0-9]+)\s+([0-9]+)\]\s+([0-9\.\-]+)\s+([A-Za-z\>\<]+)\s+\[([A-Z]*)\]',l)
            if not p:

                continue
            sound_beg=p.group(1)

            sound_end=p.group(2)

            parse_score=p.group(3)

            lemma=p.group(4)
            try:
                base=BaseDict[lemma.replace('AE', 'ä').replace('OE', 'ö').replace('AA', 'å').lower()]
            except KeyError:
                base=lemma.replace('AE', 'ä').replace('OE', 'ö').replace('AA', 'å').lower()
            if type(base) is list:
                base=base[0]

            Parse[p_idx]=[base, sound_beg, sound_end, lemma, parse_score]
            if base in WIndex:
                if type(WIndex[base]) is list:
                    WIndex[base].append(p_idx)
                else:
                    WIndex[base]=[WIndex[base]]
                    WIndex[base].append(p_idx)
            else:
                WIndex[base]=p_idx
            p_idx=p_idx+1
        return Parse, WIndex








def check_julius(wavfilelist):
    """
            check whether the wavfiles in wavfilelist have an associated julius output
            __________
            Parameters:
                wavfilelist: a list of wav filenames
            __________
            Returns:
                checklist: a list of zeros and ones of the same length as wavfilelist, 1 means has been processed


            """

    checklist=np.zeros([len(wavfilelist),1])
    for i in range(len(wavfilelist)):

        stemre=re.match('(.+)\.wav$',wavfilelist[i])
        if stemre:
            stem=stemre.group(1)

        if os.path.exists(stem+'.out'):
            checklist[i]=1

    return checklist





def prep_wav(wavlist):
     """
            converts wavfiles given in wavlist to format compatible with Julius recogniser
            __________
            Parameters:
                wavlist: a list of wav filenames
    


            """

    import soundfile as sf
    i=0
    with open(wavlist, 'r') as f:
        for wfile in f:
            if i%1000==0:
                print(i)
            stemre=re.search('^(.+)\.wav$', wfile.strip())
            stem=stemre.group(1)
            try:
                x, Fs = sf.read(wfile.strip())
                y=x[0:,1]
                sf.write(stem+'_prepped.wav', y, Fs)
            except RuntimeError:
                continue

            i=i+1


