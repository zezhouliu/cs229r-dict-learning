import normalize

import numpy as np

from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.externals import joblib
from sklearn import svm

prefix = "intermediates/KSVD_"
capacity = 10000

def train_kmeans(encodings, k):
    """
    Trains a dictionary with k-atoms using K-Means clusters
    """
    kmean = KMeans(n_clusters=k)

    model = kmean.fit(encodings)

    return model

def train_ksvd(encodings, k, iters=10):
    """
    Trains a dictionary with k-atoms using K-SVD
    """
    ksvd = TruncatedSVD(n_components=k)
    model = ksvd.fit(encodings)

    return model

def matching_pursuit(y, Dt, k, x):
    """
    Computes a sparse code z such that:
    y = Dx
    """

    max_inner_product = 0
    max_index = None

    for i in xrange(len(Dt)):
        di = Dt[i]
        ip = np.dot(di, y)
        if abs(ip) > abs(max_inner_product):
            max_inner_product = ip
            max_index = i

    # Let's try to break out early
    # if the inner_product is very very small
    if max_inner_product < 0.01:
        return

    if max_index != None:
        x[max_index] += max_inner_product

    if k > 1:
        return matching_pursuit(y - (max_inner_product * np.transpose(Dt[max_index])), Dt, k - 1, x)

    return x

def orthogonal_matching_pursuit(y, D):
    omp = OrthogonalMatchingPursuit()
    omp.fit(D, y)
    return omp

if __name__ == '__main__':
    """
    Loads the textual encodings, and then trains a model using K-clusters.
    Each cluster represents an atom in our dictionary.
    """

    # num_clusters = 100
    k = 200

    # Load the dictionary
    dictionary, dictionary_list = normalize.load_dictionary("1k.txt")
    print "loaded dict"

    # Generate encodings and track stars
    encodings, stars = normalize.read_data("all.json", dictionary, 0, capacity)
    normalized = normalize.standardize(encodings)

    np.save(prefix + str(capacity) + "og-means", normalized)
    print "generated encodings"

    ##### KSVD #####
    # Perform PCA for the eigenvalues/vectors
    model = train_ksvd(normalized, k)
    dict_row = model.components_
    dict_col = np.transpose(dict_row)

    ##### TRUNCATED SVD #####
    # Need to get x's for each of the y's in normalized
    XT = model.transform(normalized)

    clf = svm.SVC()
    clf.fit(XT, stars)

    print "Truncated Training score: ", clf.score(XT, stars)

    ##### OMP SVD #####
    omp = orthogonal_matching_pursuit(np.transpose(normalized), dict_col)
    omp_XT = omp.coef_

    omp_clf = svm.SVC()
    omp_clf.fit(omp_XT, stars)


    print "OMP Training score: ", omp_clf.score(omp_XT, stars)

    # Test it on our training set
    test_encodings, test_stars = normalize.read_data("test.json", dictionary, 0, 10000)

    # Normalize
    test_encodings = normalize.standardize(test_encodings)
    test_XT = model.transform(test_encodings)
    print "Truncated Testing score: ", clf.score(test_XT, test_stars)

    omp_test = orthogonal_matching_pursuit(np.transpose(test_encodings), dict_col)
    omp_test_XT = omp_test.coef_

    print "OMP Testing score: ", omp_clf.score(omp_test_XT, test_stars)

