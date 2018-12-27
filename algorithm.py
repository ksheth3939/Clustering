"""
Primary algorithm for k-Means clustering
"""
import math
import random
import numpy


import checks
import dataset
import https://www.linkedin.com/in/kunal-sheth-374069176cluster


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.
    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset which this is a clustering of
        _clusters [list of Cluster]: the clusters in this clustering (not empty)
    """

    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition seeds is None, or a list of k valid indices into dset.
        """
        assert k > 0
        assert k <= dset.getSize()
        assert seeds == None or checks.is_point(seeds)
        if (seeds != None):
            assert len(seeds) == k

        self._dataset = dset
        self._clusters = []
        if (seeds == None):
            a = random.sample(self._dataset.getContents(), k)
            for x in a:
                self._clusters.append(cluster.Cluster(self._dataset, x))
        else:
            for y in seeds:
                self._clusters.append(cluster.Cluster(self._dataset,
                self._dataset.getPoint(y)))


    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns _clusters directly.  Any changes made to this
        list will modify the set of clusters.
        """
        return self._clusters

    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        Parameter point: The point to compare.
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the dataset.
        """
        assert checks.is_point(point)
        assert len(point) == self._dataset.getDimension()
        max = math.inf
        a = 0
        for z in self.getClusters():
            min = z.distance(point)
            if (min < max):
                max = min
                a = z
        return a


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """

        for x in self.getClusters():
            x.clear()

        for y in range(0,len(self._dataset.getContents())):
            self._nearest(self._dataset.getPoint(y)).addIndex(y)

    def _update(self):
        """
        Returns true if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters'.  When it is done, it
        checks whether any of them have changed. It then returns the appropriate value.
        """
        a = True
        for x in self.getClusters():
            if (not x.update()):
                a = False
        return a


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks if
        the algorithm has converged and returns the appropriate value.
        """
        self._partition()
        return self._update()

    def run(self, maxstep):
        """
        Continues clustering until either it converges or maxstep step

        Parameter maxstep: the maximum number of steps to try
        Precondition: maxstep is an int >= 0
        """
        assert type(maxstep) == int
        assert maxstep >= 0

        for x in range(0, maxstep):
            if (self.step()):
                return 0
