#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NSTtools: helper functions for NST corpus analysis, mostly calling Praat scripts
(C) Nadja Althaus 2022
"""


import NSTcorpus
import subprocess
import re
import wave

def playwav(wavfilename):
     """
        Uses praat to play a wav file
              
        Parameters
        ----------
        wavfilename: file name ending in .wav

        
     """  
    subprocess.call(["/Applications/Praat.app/Contents/MacOS/Praat", "--run", "playaudio.praat", wavfilename])

def playwav_many( NSTwavfilenames, NSTtranscripts, l=list()):
    """
        Like playwav but for a list of wavfiles, plays items with indices given in l,
        prints transcript on std out
              
        Parameters
        ----------
        NSTwavfilenames: list of file names ending in .wav
        NSTtranscripts: list of str, transcripts from NST corpus
        l: list of int, indices in range(0, len(NSTwavfilenames))

       
     """  
    
    
    for idx in l:
        audiofile=NSTwavfilenames[idx]
        print('Playing wav file.\nTranscript:'+NSTtranscripts[idx])
        subprocess.call(["/Applications/Praat.app/Contents/MacOS/Praat", "--run", "playaudio.praat", audiofile])
    
        print('done.')




def cutwav(wavfilename, cutpoint1, cutpoint2, outfilename):
    """
        Uses a praat script to cut a wavfile, writes output to outfilename
              
        Parameters
        ----------
        wavfilename: a file name ending in .wav
        cutpoint1, cutpoint2: timestamps for left and right edge of segment to be cut in sec
        outfilename: a filename for the output segment, .wav

       
        
     """  
    print('cutting wav file')
    subprocess.call(["/Applications/Praat.app/Contents/MacOS/Praat", "--run", "cutwav.praat", wavfilename, cutpoint1, cutpoint2, outfilename])


    
def getpitch(wavfilename):
        """
        Obtain f0 contours from praat script, write to text file
              
        Parameters
        ----------
        wavfilename: a file name ending in .wav
        
        Returns
        ----------
        outfilename: text file name ending in '_pitch.txt'
        
     """  
    fnr=re.search('(.*)\.wav$', wavfilename)
    stem=fnr.group(1)
    outfilename=stem+'_pitch.txt'
    of=open(outfilename,'w')
    of.close()
    subprocess.call(["/Applications/Praat.app/Contents/MacOS/Praat", "--run", "getpitch.praat", wavfilename, outfilename])
    return outfilename

