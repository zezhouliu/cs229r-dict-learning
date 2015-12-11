import argparse
import collections
import csv
import json
import operator

import numpy as np

def load_dictionary(dict_file_path):
    dictionary = {}
    word_counts = {}
    dictionary_list = []
    with open(dict_file_path) as fin:
        dictionary_list = [line.rstrip('\n') for line in fin]
        for idx in xrange(len(dictionary_list)):
            dictionary[dictionary_list[idx]] = idx
            word_counts[dictionary_list[idx]] = 0

    return dictionary, dictionary_list, word_counts

def shrink_dictionary(dict_file_path, dictionary):
    with open(dict_file_path, 'wb+') as fout:
        sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
        for idx in xrange(len(sorted_dict)):
            if sorted_dict[idx][1] == 0:
                break
            fout.write(sorted_dict[idx][0] + "\n")

    return

def encode(dictionary, sentence, count_dict):
    """
    Encodes the sentence into a vector where the value v at position x
    corresponds to the number of occurences of the word dictionary
    """
    length = len(dictionary_list)
    encoding = np.zeros(length)

    words = sentence.split()
    for word in words:
        lower_word = word.lower()
        if lower_word in dictionary:
            encoding[dictionary[lower_word]] += 1
            count_dict[lower_word] += 1

    return encoding

def read_data (json_file_path, dictionary, word_counts):
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
            line_contents = json.loads(line)
            encoding = encode(dictionary, line_contents["text"], word_counts)
            # Ignore the ones with 0 encoding
            if np.linalg.norm(encoding) == 0:
                continue
            star = line_contents["stars"]

            # Track the encodings and stars
            # encodings.append(encoding)
            # stars.append(int(star))

    return np.asarray(encodings), np.asarray(stars)

def normalize_encodings(encodings):
    for i in xrange(len(encodings)):
        encoding = encodings[i]
        norm = np.linalg.norm(encoding)
        if norm == 0:
            norm = 1
        encodings[i] = encoding / norm

    return encodings

def PCA(encodings):
    # Calculate the mean for each dimension
    means = np.zeros(len(encodings))
    for i in xrange(len(encodings)):
        means[i] = np.mean(encodings[i,:])

    print "calculated means"
    np.save("means", means)

    # Subtract the mean from the data
    for dim in xrange(len(encodings)):
        for i in xrange(len(encodings[dim,:])):
            encodings[dim,:][i] -= means[dim]

    np.save("encodings-means", encodings)

    print "calculating cov"
    cov_mat = np.cov(encodings)
    np.save("cov_matrix", cov_mat)

    print "calculating eig"

    eig_val, eig_vec = np.linalg.eig(cov_mat)
    np.save("eig_vals", eig_val)
    np.save("eig_vec", eig_vec)

    return eig_val, eig_vec

if __name__ == '__main__':
    # Load the dictionary
    dictionary, dictionary_list, word_counts = load_dictionary("data/10k-english.txt")

    # Generate encodings and track stars
    encodings, stars = read_data("all.json", dictionary, word_counts)

    shrink_dictionary("data/all_dict.txt", word_counts)
