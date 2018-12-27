"""
Cluster class for k-Means clustering
"""
import math
import random
import numpy


import checks
import dataset


class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.
    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset this cluster is a subset of
        _indices [list of int]: the indices of this cluster's points in the dataset
        _centroid [list of numbers]: the centroid of this cluster
    EXTRA INVARIANTS:
        len(_centroid) == _dataset.getDimension()
        0 <= _indices[i] < _dataset.getSize(), for all 0 <= i < len(_indices)
    """
    def __init__(self, dset, centroid):
        """
        Initializes a new empty cluster whose centroid is a copy of <centroid>

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a list of ds.getDimension() numbers
        """
        assert checks.is_point(centroid)
        assert isinstance(dset, dataset.Dataset)

        self._dataset = dset
        self._indices = []
        self._centroid = []
        for x in centroid:
            self._centroid.append(x)


    def getCentroid(self):
        """
        Returns the centroid of this cluster.

        This getter method is to protect access to the centroid.
        """
        return self._centroid


    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the attribute _indices directly.  Any changes made to this
        list will modify the cluster.
        """
        return self._indices


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int in the range 0.._dataset.getSize()-1.
        """
        assert index >= 0
        assert index <= self._dataset.getSize()-1

        count = 0
        for x in self.getIndices():
            if (index == x):
                count = count + 1
        if (count == 0):
            self._indices.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leave the centroid unchanged.
        """
        self.getIndices().clear()


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.
        The result is a list of list of numbers.  It has to be computed from the indices.
        """
        x = []
        for y in self.getIndices():
            x.append(self._dataset.getPoint(y))
        return x

    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the centroid.
        """
        assert checks.is_point(point)

        count = 0
        for x in range(0, len(point)):
            count = count + (point[x] - self._centroid[x])**2
        return count**(1/2)


    def getRadius(self):
        """
        Returns the maximum distance from any point in this cluster, to the centroid.

        This method loops over the contents to find the maximum distance from
        the centroid.  If there are no points in this cluster, it returns 0.
        """
        max = 0
        x = 0
        for x in self.getIndices():
            x = self.distance(self._dataset.getPoint(x))
            if (x > max):
                max = x
        return max


    def update(self):
        """
        Returns True if the centroid remains the same after recomputation; False otherwise.

        If there are no points in the cluster, the centroid. does not change.
        """
        a = []
        sum = 0
        for x in range(0,len(self.getContents()[0])):
            sum = 0
            for y in range(0, len(self.getContents())):
                  sum = sum + self.getContents()[y][x] + 0.0
            sum = sum/len(self.getIndices())
            a.append(sum)

        if (numpy.allclose(a, self._centroid)):
            self._centroid = a
            return True

        self._centroid = a
        return False

    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)


    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.
        """
        return str(self.__class__) + str(self)
