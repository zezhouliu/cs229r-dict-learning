import argparse
import collections
import csv
import json
import operator

import numpy as np

def load_dictionary(dict_file_path):
    dictionary = {}
    dictionary_list = []
    with open(dict_file_path) as fin:
        dictionary_list = [line.rstrip('\n') for line in fin]
        for idx in xrange(len(dictionary_list)):
            dictionary[dictionary_list[idx]] = idx

    return dictionary, dictionary_list

def encode(dictionary, sentence):
    """
    Encodes the sentence into a vector where the value v at position x
    corresponds to the number of occurences of the word dictionary
    """
    length = len(dictionary)
    encoding = np.zeros(length)

    words = sentence.split()
    for word in words:
        lower_word = word.lower()
        if lower_word in dictionary:
            encoding[dictionary[lower_word]] += 1

    return encoding

def read_data (json_file_path, dictionary, offset, num_data):
    """Read in the json dataset file and parses the data.
        - Removes punctuation
        - Returns a fixed length encoding for each string.
    """
    encodings = []
    stars = []
    with open(json_file_path) as fin:
        count = 0
        for line in fin:
            # print count
            count += 1
            if count < offset:
                continue
            if count == offset + num_data:
                break
            line_contents = json.loads(line)
            encoding = encode(dictionary, line_contents["text"])
            # Ignore the ones with 0 encoding
            if np.linalg.norm(encoding) == 0:
                continue
            star = line_contents["stars"]

            # Track the encodings and stars
            encodings.append(encoding)
            stars.append(int(star))

    return np.asarray(encodings), np.asarray(stars)

def standardize(encodings):
    # Calculate the mean for each dimension
    means = np.zeros(len(encodings))
    for i in xrange(len(encodings)):
        means[i] = np.mean(encodings[i,:])

    print "Calculated means"

    # Subtract the mean from the data
    for dim in xrange(len(encodings)):
        for i in xrange(len(encodings[dim,:])):
            encodings[dim,:][i] -= means[dim]

    encodings = normalize_encodings(encodings)

    return encodings

def normalize_encodings(encodings):
    for i in xrange(len(encodings)):
        encoding = encodings[i]
        norm = np.linalg.norm(encoding)
        if norm == 0:
            norm = 1
        encodings[i] = encoding / norm

    return encodings
