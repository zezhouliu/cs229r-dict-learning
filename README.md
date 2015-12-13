# cs229r-dict-learning

## Data
The data files for this project was obtained via the Yelp Dataset Challenge.
The full data set can be found online on their [website](http://www.yelp.com/dataset_challenge).

We work mostly with a subset of this data--specifically the reviews in the data set.
We added some pre-processing of the data on top of the reviews.  Please find the
reviews available via this [dropbox link](https://www.dropbox.com/sh/avcyh1uoxl3om2t/AAA3auiTLcrLJz8_etk_ydf2a?dl=0),
and save the reviews and tips in the "data/" directory. You will want to save `all.json` in the home directory.

As a result, please make sure you have the following in your data directory:

`review.json`, `tip.json`, `100k_dict.txt`, and `10k-english.txt`

In the home directory, please make sure the following data files are present:

`1k.txt`, `400.txt`, `5000.txt`, `all.json` and `test.json`


## Procedure
This project contains multiple procedures: preprocess, filter_words, and the algorithms.

### preprocess.py
`preprocess.py` produces a filtered json data by parsing out only the "text" and "stars" 
features in the json and saving it in another file.  The input file is given as a command line 
argument, and the output file can be updated in the code.

In the `read_and_write_file` function, there is a `count` variable that can be updated that will
allow you to modify which parts of the `review.json` data will be parsed out.  The current code will
skip to the 500k data entry, and then save the next 10k data entries.  Also, on the bottom of the file,
the variable `out_json_file` indicates the outfile name. This code is used to generate the
training and  test data for our classifier.  The code has already been run to generate `all.json` and
`test.json` and so does not need to be run again. But if you want to run it, you can use:

`python preprocess.py data/review.json`

### filter_words.py
`filter_words.py` is used to filter out the top k-words in the english text that occur in the review corpus.
What it does is it reads in the data, and then tracks the top k-words that exist in the reviews that also 
exist in the english dictionary. It outputs these words in descending.  This is useful so that we can
use just the top k-words when encoding our reviews.  It has already been run, so we do not need to run again.

### PCA.py KSVD.py
PCA and KSVD implement their corresponding algorithms in their files.  Some parameters you can tweak are the datasets
they input (they currently take in `all.json`), the test data (they currently take in `test.json`), the size of the 
dictionaries (the dictionary length is equal to the encoding length of each review) by updating the input
dictionary file.  You can also update the number of dictionary atoms in the dctionary by updating `top_k` in the
PCA.py file and the `k` variable in the KSVD file.

### ER-SpUD
Since ER-SpUD requires a linear algebra solver, we attemped to use Matlab.  The driver is partially implemented
`erspud.m` and `erspud-driver.m`, but is currently incomplete.


