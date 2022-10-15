# Using LSTM deep neural networks for prosody analysis in a Swedish speech corpus

(C) Nadja Althaus, 2022

This repository contains a collection of Jupyter notebooks to (a) extract pitch contours from the NST spoken Swedish corpus,
(b) train an LSTM network to classify pitch patterns on the basis of grammatical assignment to Accent 1 or 2, and (c) visualise and explore
the learned representation. The project is a work in progress.

The speech corpus can be obtained from the [National Library of Norway] (https://www.nb.no/sprakbanken/en/resource-catalogue/oai-nb-no-sbr-56/).

[NSTcreate.ipynb] (https://github.com/nadjaalthaus/AccentLSTM/blob/main/NSTcreate.ipynb) 
Here we create a database of approx. 120,000 pitch accent patterns, from disyllabic nouns found in the NST corpus.

[NSTPitchPrep.Rmd](https://github.com/nadjaalthaus/AccentLSTM/blob/main/NSTPitchPrep.Rmd)
The final preprocessing step: normalisation and smoothing.

[CorpusLSTM.ipynb]  (https://github.com/nadjaalthaus/AccentLSTM/blob/main/CorpusLSTM.ipynb)
In this notebook we train an LSTM deep network to classify pitch patterns according to their "grammatical" assignment to Accent 1 and 2.

[ModelExploration.ipynb] (https://github.com/nadjaalthaus/AccentLSTM/blob/main/ModelExploration.ipynb)
We visualise the LSTM model's hidden unit space and explore which segments of the input patterns contribute most to the classification.

