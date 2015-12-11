import normalize

import argparse
import collections
import csv
import json
import operator

import numpy as np

from sklearn.externals import joblib
from sklearn import svm

prefix = "intermediates/PCA_"
capacity = 10000

def PCA(encodings):
    """
    Performs PCA on the encodings.
    First, it calculates the mean for the data set along the dimensions.
    Then it centers the data by subtracting the mean from each data point.
    Then, it scales the data into a unit vector.
    This process is called standardization.
    Then it calculates the eigenvalues/eigenvectors using eigenvalue decomposition
    on the covariance matrix
    """

    print "Calculated normalization"
    encodings = normalize.standardize(encodings)
    np.save(prefix + str(capacity) + "normalized", encodings)

    print "calculating cov"
    cov_mat = np.cov(encodings)
    np.save(prefix + str(capacity) + "cov_matrix", cov_mat)

    print "calculating eig"

    eig_vals, eig_vecs = np.linalg.eig(cov_mat)
    idx = eig_vals.argsort()[::-1]
    eig_vals = eig_vals[idx]
    eig_vecs = eig_vecs[:,idx]

    np.save(prefix + str(capacity) + "eig_vals", eig_vals)
    np.save(prefix + str(capacity) + "eig_vecs", eig_vecs)

    return eig_val, eig_vec

if __name__ == '__main__':
    # Load the dictionary
    dictionary, dictionary_list = normalize.load_dictionary("1k.txt")
    print "loaded dict"

    # Generate encodings and track stars
    encodings, stars = normalize.read_data("all.json", dictionary, 0, capacity)
    np.save(prefix + str(capacity) + "og-means", encodings)
    print "generated encodings"

    # Perform PCA for the eigenvalues/vectors
    eig_vals, eig_vecs = PCA(encodings)

    top_k = 100
    k_eig_vals = eig_vals[:top_k]
    k_eig_vecs = eig_vecs[:top_k]

    # for i in xrange(len(k_eig_vals)):
        # print i, k_eig_vals[i]

    normalized = encodings

    final = np.dot(k_eig_vecs, normalized)

    # Need to pass in each encoding row-wise
    final_t = np.transpose(final)
    clf = svm.SVC()
    clf.fit(final_t, stars)

    # Save our model
    joblib.dump(clf, "pca_clf.pkl")

    print "Training score: ", clf.score(final_t, stars)

    # Test it on our training set
    test_encodings, test_stars = normalize.read_data("test.json", dictionary, 0, 10000)

    # Normalize
    test_encodings = normalize.standardize(test_encodings)
    final_test = np.dot(k_eig_vecs, test_encodings)
    final_test_t = np.transpose(final_test)
    print "Testing score: ", clf.score(final_test_t, test_stars)


