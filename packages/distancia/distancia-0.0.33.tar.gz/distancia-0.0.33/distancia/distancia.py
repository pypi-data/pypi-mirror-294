#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  distancia.py
#  
#  Copyright 2024 yves <yves.mercadier@...>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from .mainClass import Distance
from .distance import *
#from .tools     import *

class CustomDistanceFunction(Distance):
    """
    A class to compute custom distance between two data points using a user-defined function.
    """
    def __init__(self):
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()


    def __init__(self, func=Euclidean()):
        """
        Initialize the CustomDistanceFunction class with a user-defined function.

        Parameters:
        func (function): A function that takes two inputs (data points) and returns a distance metric.
        """
        if not callable(func):
            raise ValueError("The provided custom function must be callable.")
        self.func = func

    def calculate(self, data1, data2):
        """
        Compute the distance between two data points using the custom function.

        Parameters:
        data1: The first data point.
        data2: The second data point.

        Returns:
        The result of the custom function applied to data1 and data2.
        """
        return self.func(data1, data2)

import pandas as pd
import numpy as np

class IntegratedDistance:
    def __init__(self, func=Euclidean()):
        """
        Initialize the IntegratedDistance class with a distance function.
        
        Parameters:
        func (callable): A function that takes two points and returns a distance. 
                         Default is Euclidean distance.
        """
        self.func = func

    def calculate(self, point1, point2):
        """
        Compute the distance between two points using the specified distance function.
        
        Parameters:
        point1, point2: The points between which to compute the distance. Can be tuples, lists, or numpy arrays.
        
        Returns:
        float: The computed distance.
        """
        return self.func(point1, point2)

    def apply_to_dataframe(self, df, col1, col2, result_col='distance'):
        """
        Apply the distance function to columns of a pandas DataFrame.
        
        Parameters:
        df (pandas.DataFrame): The DataFrame containing the points.
        col1 (str): The name of the first column containing the points.
        col2 (str): The name of the second column containing the points.
        result_col (str): The name of the column to store the computed distances.
        
        Returns:
        pandas.DataFrame: The DataFrame with an additional column containing the distances.
        """
        df[result_col] = df.apply(lambda row: self.calculate(row[col1], row[col2]), axis=1)
        return df

class IntegratedDistance:
    def __init__(self, func=Euclidean()):
        """
        Initialize the IntegratedDistance class with a distance function.
        
        Parameters:
        func (callable): A function that takes two points and returns a distance. 
                         Default is Euclidean distance.
        """
        self.func = func

    def calculate(self, point1, point2):
        """
        Compute the distance between two points using the specified distance function.
        
        Parameters:
        point1, point2: The points between which to compute the distance. Can be tuples, lists, or numpy arrays.
        
        Returns:
        float: The computed distance.
        """
        return self.func(point1, point2)

    def apply_to_dataframe(self, df, col1, col2, result_col='distance'):
        """
        Apply the distance function to columns of a pandas DataFrame.
        
        Parameters:
        df (pandas.DataFrame): The DataFrame containing the points.
        col1 (str): The name of the first column containing the points.
        col2 (str): The name of the second column containing the points.
        result_col (str): The name of the column to store the computed distances.
        
        Returns:
        pandas.DataFrame: The DataFrame with an additional column containing the distances.
        """
        df[result_col] = df.apply(lambda row: self.calculate(row[col1], row[col2]), axis=1)
        return df

    def apply_to_sklearn(self, X, Y=None):
        """
        Apply the distance function within a scikit-learn pipeline.
        
        Parameters:
        X (numpy array or pandas DataFrame): The data for which to compute distances.
        Y (numpy array or pandas DataFrame, optional): Another data set to compare with.
        
        Returns:
        numpy.array: An array of computed distances.
        """
        if Y is None:
            Y = X
        
        distances = np.zeros((X.shape[0], Y.shape[0]))
        for i in range(X.shape[0]):
            for j in range(Y.shape[0]):
                distances[i, j] = self.calculate(X[i], Y[j])
                
        return distances

class DistanceMatrix:
    def __init__(self, data_points, metric=Euclidean()):
        """
        Initializes the DistanceMatrix class.

        Parameters:
        - data_points: List or array-like, a collection of data points where each point is an iterable of coordinates.
        - metric: str, the distance metric to be used (e.g., 'euclidean', 'cosine', 'manhattan'). The metric must be one of the predefined metrics in the `distancia` package.
        """
        self.data_points = data_points
        self.metric = metric
        self.distance_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self):
        """
        Computes the distance matrix for the provided data points using the specified metric.

        Returns:
        - A 2D list representing the distance matrix where element (i, j) is the distance between data_points[i] and data_points[j].
        """
        num_points = len(self.data_points)
        matrix = [[0.0] * num_points for _ in range(num_points)]

        for i in range(num_points):
            for j in range(i + 1, num_points):
                distance = self.metric.calculate(self.data_points[i], self.data_points[j])
                matrix[i][j] = distance
                matrix[j][i] = distance

        return matrix

    def get_matrix(self):
        """
        Returns the computed distance matrix.
        """
        return self.distance_matrix

import concurrent.futures
from functools import partial
import multiprocessing

class ParallelandDistributedComputation:
    def __init__(self, data_points, metric):
        """
        Initializes the ParallelDistanceCalculator with a set of data points and a distance metric.

        :param data_points: A list or array of data points.
        :param metric: A callable that computes the distance between two data points.
        """
        self.data_points = data_points
        self.metric = metric

    def compute_distances_parallel(self, reference_point=None, max_workers=None, use_multiprocessing=False):
        """
        Computes distances in parallel between the reference point and all data points or pairwise among all data points.

        :param reference_point: A single data point to compare with all other data points. 
                                If None, computes pairwise distances among all data points.
        :param max_workers: The maximum number of workers to use for parallel computation.
                            If None, it will use the number of processors on the machine.
        :param use_multiprocessing: If True, uses multiprocessing for parallel computation.
                                    If False, uses multithreading.
        :return: A list of computed distances.
        """
        if reference_point is not None:
            compute_func = partial(self.metric.calculate, reference_point)
            data_iterable = self.data_points
        else:
            data_iterable = ((self.data_points[i], self.data_points[j]) for i in range(len(self.data_points)) for j in range(i + 1, len(self.data_points)))
            compute_func = lambda pair: self.metric.calculate(*pair)

        if use_multiprocessing:
            with multiprocessing.Pool(processes=max_workers) as pool:
                distances = pool.map(compute_func, data_iterable)
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                distances = list(executor.map(compute_func, data_iterable))

        return distances

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from collections import defaultdict

class OutlierDetection:
    def __init__(self, data_points, metric=Euclidean(), threshold=2.0):
        """
        Initialize the OutlierDetection class.

        :param data_points: A list of data points, where each data point is a list or tuple of numeric values.
        :param metric: The distance metric to use for outlier detection. Supported metrics: 'euclidean', 'manhattan', 'mahalanobis'.
        :param threshold: The threshold value for determining outliers. Points with distances greater than this threshold times the standard deviation from the centroid are considered outliers.
        """
        self.data_points = data_points
        self.metric = metric
        self.threshold = threshold
        self.centroid = self._calculate_centroid()
        self.distances = self._calculate_distances()

    def _calculate_centroid(self):
        """
        Calculate the centroid of the data points.

        :return: The centroid as a list of numeric values.
        """
        n = len(self.data_points)
        centroid = [sum(dim)/n for dim in zip(*self.data_points)]
        return centroid

    def _calculate_distances(self):
        """
        Calculate the distances of all points from the centroid using the specified metric.

        :return: A list of distances as floats.
        """
        distances = []
        for point in self.data_points:
            distance = self.metric.calculate(point, self.centroid)
            distances.append(distance)
        return distances

    def detect_outliers(self):
        """
        Detect outliers based on the distance from the centroid.

        :return: A list of outliers, where each outlier is a tuple containing the point and its distance from the centroid.
        """
        mean_distance = sum(self.distances) / len(self.distances)
        std_distance = (sum((d - mean_distance) ** 2 for d in self.distances) / len(self.distances))**0.5

        outliers = []
        for i, distance in enumerate(self.distances):
            if distance > mean_distance + self.threshold * std_distance:
                outliers.append((self.data_points[i], distance))

        return outliers


    
class BatchDistance:
    def __init__(self, points_a, points_b, metric):
        """
        Initialize the BatchDistance class with two sets of points and a distance metric.

        :param points_a: A list of tuples representing the first set of points.
        :param points_b: A list of tuples representing the second set of points.
        :param metric: A string representing the distance metric to be used ('euclidean', 'manhattan', etc.).
        """
        self.points_a = points_a
        self.points_b = points_b
        self.metric = metric

    def compute_batch(self):
        """
        Compute the distances for all pairs in the two sets of points.

        :return: A list of distances for each pair of points.
        """
        if len(self.points_a) != len(self.points_b):
            raise ValueError("The two point sets must have the same length.")

        distances = []
        for point1, point2 in zip(self.points_a, self.points_b):
            distance = self.metric.calculate(point1, point2)
            distances.append(distance)

        return distances


import time

class ComprehensiveBenchmarking:
    def __init__(self, metrics, data, repeat=1):
        """
        Initialize the ComprehensiveBenchmarking class.

        :param metrics: List of metric functions to benchmark.
        :param data: The data points to use in the benchmarking.
        :param repeat: Number of times to repeat each metric calculation for averaging.
        """
        self.metrics = metrics
        self.data    = data
        self.repeat  = repeat
        self.results = {}

    def run_benchmark(self):
        """
        Run the benchmark for each metric on the provided data.

        :return: Dictionary with metrics as keys and their average computation time as values.
        """
        for metric in self.metrics:
            start_time = time.time()
            for _ in range(self.repeat):
                _ = [metric.calculate(x, y) for x, y in self.data]
            end_time = time.time()
            average_time = (end_time - start_time) / self.repeat
            self.results[metric.__class__.__name__] = average_time

        return self.results

    def print_results(self):
        """
        Print the benchmarking results in a readable format.
        """
        for metric, time_taken in self.results.items():
            print(f"Metric: {metric}, Average Time: {time_taken:.6f} seconds")


class DistanceMetricLearning:
    def __init__(self, data, labels, method='lmnn', **kwargs):
        """
        Initialize the DistanceMetricLearning class.

        Parameters:
        - data: array-like, shape (n_samples, n_features)
            The input data points.
        - labels: array-like, shape (n_samples,)
            The class labels or targets associated with the data points.
        - method: str, optional (default='lmnn')
            The distance metric learning method to use. Options are 'lmnn', 'itml', 'nca', etc.
        - kwargs: additional keyword arguments specific to the chosen method.
        """
        self.data = data
        self.labels = labels
        self.method = method.lower()
        self.kwargs = kwargs
        self.metric = None

    def fit(self):
        """
        Fit the distance metric to the data using the specified method.
        """
        if self.method == 'lmnn':
            self.metric = self._learn_lmnn()
        elif self.method == 'itml':
            self.metric = self._learn_itml()
        elif self.method == 'nca':
            self.metric = self._learn_nca()
        else:
            raise ValueError(f"Method {self.method} is not supported.")
    
    def transform(self, X):
        """
        Transform the data using the learned metric.

        Parameters:
        - X: array-like, shape (n_samples, n_features)
            The data to transform.

        Returns:
        - X_transformed: array-like, shape (n_samples, n_features)
            The data transformed using the learned metric.
        """
        if self.metric is None:
            raise ValueError("The model needs to be fitted before transformation.")
        return self.metric.transform(X)
    
    def _learn_lmnn(self):
        # Placeholder function for learning LMNN
        # In practice, you would use a library like metric-learn, or implement LMNN from scratch.
        from metric_learn import LMNN
        lmnn = LMNN(**self.kwargs)
        lmnn.fit(self.data, self.labels)
        return lmnn

    def _learn_itml(self):
        # Placeholder function for learning ITML
        from metric_learn import ITML
        itml = ITML(**self.kwargs)
        itml.fit(self.data, self.labels)
        return itml

    def _learn_nca(self):
        # Placeholder function for learning NCA
        from sklearn.neighbors import NeighborhoodComponentsAnalysis
        nca = NeighborhoodComponentsAnalysis(**self.kwargs)
        nca.fit(self.data, self.labels)
        return nca

    def get_metric(self):
        """
        Get the learned metric.
        
        Returns:
        - metric: the learned metric object
        """
        if self.metric is None:
            raise ValueError("The model needs to be fitted before accessing the metric.")
        return self.metric

class MetricFinder:
	def __init__(self):
		"""
		Initialize the MetricFinder class.
		"""
		self.list_metric=[]

	def find_metric(self, point1, point2):
		"""
		Determines the most appropriate metric for the given points based on their structure.

		Parameters:
		point1: The first point (can be a list, string, or other iterable).
		point2: The second point (can be a list, string, or other iterable).

		Returns:
		str: The name of the most appropriate metric.
		"""
		if isinstance(point1, str) and isinstance(point2, str):self.find_string_metric(point1, point2)
		elif isinstance(point1, (list)) and isinstance(point2, (list)):
			self.list_metric.append(LongestCommonSubsequence().__class__.__name__)

			if all(isinstance(x, (tuple)) for x in point1) and all(isinstance(x, (tuple)) for x in point2):
				self.list_metric.append(Frechet().__class__.__name__)

			if all(isinstance(x, (float,int)) for x in point1) and all(isinstance(x, (float,int)) for x in point2):
				if len(point1)==len(point2):
					self.list_metric.append(Euclidean().__class__.__name__)
					self.list_metric.append(Manhattan().__class__.__name__)
					self.list_metric.append(Minkowski().__class__.__name__)
					self.list_metric.append(L1().__class__.__name__)
					self.list_metric.append(L2().__class__.__name__)
					self.list_metric.append(Canberra().__class__.__name__)
					self.list_metric.append(BrayCurtis().__class__.__name__)
					self.list_metric.append(Gower().__class__.__name__)
					self.list_metric.append(Pearson().__class__.__name__)
					self.list_metric.append(Spearman().__class__.__name__)
					self.list_metric.append(CzekanowskiDice().__class__.__name__)
					self.list_metric.append(MotzkinStraus().__class__.__name__)
					self.list_metric.append(EnhancedRogersTanimoto().__class__.__name__)
					self.list_metric.append(DynamicTimeWarping().__class__.__name__)
					self.list_metric.append(CosineInverse().__class__.__name__)
					self.list_metric.append(CosineSimilarity().__class__.__name__)
					self.list_metric.append(GeneralizedJaccard().__class__.__name__)
					self.list_metric.append(Chebyshev().__class__.__name__)
					

			if all(isinstance(x, (int)) for x in point1) and all(isinstance(x, (int)) for x in point2):
					self.list_metric.append(KendallTau().__class__.__name__)
					
			if all(check_bin(x) for x in point1) and all(check_bin(x) for x in point2) and len(point1)==len(point2):
					self.list_metric.append(Kulsinski().__class__.__name__)
					self.list_metric.append(Yule().__class__.__name__)
					self.list_metric.append(RogersTanimoto().__class__.__name__)
					self.list_metric.append(SokalMichener().__class__.__name__)
					self.list_metric.append(SokalSneath().__class__.__name__)
			if all(check_probability(x) for x in point1) and all(check_probability(x) for x in point2) and len(point1)==len(point2):
					self.list_metric.append(CrossEntropy().__class__.__name__)
					self.list_metric.append(MeanAbsoluteError().__class__.__name__)
					self.list_metric.append(MAE().__class__.__name__)
					self.list_metric.append(MeanAbsolutePercentageError().__class__.__name__)
					self.list_metric.append(MAPE().__class__.__name__)
					self.list_metric.append(MeanSquaredError().__class__.__name__)
					self.list_metric.append(MSE().__class__.__name__)
					self.list_metric.append(SquaredLogarithmicError().__class__.__name__)
					self.list_metric.append(SLE().__class__.__name__)
					self.list_metric.append(KullbackLeibler().__class__.__name__)
					self.list_metric.append(Bhattacharyya().__class__.__name__)
					self.list_metric.append(Hellinger().__class__.__name__)
					self.list_metric.append(Wasserstein().__class__.__name__)
		elif isinstance(point1, (set)) and isinstance(point2, (set)):
				if all(isinstance(x, (float,int)) for x in point1) and all(isinstance(x, (float,int)) for x in point2):
					self.list_metric.append(InverseTanimoto().__class__.__name__)
					self.list_metric.append(Tanimoto().__class__.__name__)
					self.list_metric.append(Dice().__class__.__name__)
					self.list_metric.append(Kulsinski().__class__.__name__)
					self.list_metric.append(Tversky().__class__.__name__)
					self.list_metric.append(FagerMcGowan().__class__.__name__)
					self.list_metric.append(FagerMcGowan().__class__.__name__)
					self.list_metric.append(Hausdorff().__class__.__name__)
				if all(isinstance(x, (bool)) for x in point1) and all(isinstance(x, (bool)) for x in point2):
					self.list_metric.append(Ochiai().__class__.__name__)

		return self.list_metric

	def find_string_metric(self, str1, str2):
		"""
		Determines the appropriate string-based metric.

		Parameters:
		str1: The first string.
		str2: The second string.

		Returns:
		str: The name of the most appropriate string metric.
		"""
		if len(str1) == len(str2):
			if str1.isdigit() and str2.isdigit():
				self.list_metric.append(Hamming().__class__.__name__)
				self.list_metric.append(Matching().__class__.__name__)
				
		self.list_metric.append(Jaro().__class__.__name__)
		self.list_metric.append(JaroWinkler().__class__.__name__)
		self.list_metric.append(Levenshtein().__class__.__name__)
		self.list_metric.append(DamerauLevenshtein().__class__.__name__)
		self.list_metric.append(RatcliffObershelp().__class__.__name__)
		self.list_metric.append(SorensenDice().__class__.__name__)
		self.list_metric.append(Otsuka().__class__.__name__)
		



	def find_similarity_metric(self, point1, point2):
		"""
		Determines the most appropriate similarity metric for the given points.

		Parameters:
		point1: The first point (can be a list, string, or other iterable).
		point2: The second point (can be a list, string, or other iterable).

		Returns:
		str: The name of the most appropriate similarity metric.
		"""
		if isinstance(point1, str) and isinstance(point2, str):
			return "Jaccard Similarity"
		elif isinstance(point1, (list, tuple)) and isinstance(point2, (list, tuple)):
			if all(isinstance(x, (int, float)) for x in point1) and all(isinstance(x, (int, float)) for x in point2):
				return "Cosine Similarity"
		return "Unknown Similarity Metric"



import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class APICompatibility:
    def __init__(self, distance_metric):
        """
        Initialize with a specific distance metric.
        
        :param distance_metric: A function or class from the distancia package, e.g., EuclideanDistance
        """
        self.distance_metric = distance_metric
    
    def rest_endpoint(self, host="0.0.0.0", port=5000):
        """
        Set up a REST API endpoint using Flask.
        
        :param host: Host IP address for the REST service.
        :param port: Port number for the REST service.
        """
        @app.route('/calculate_distance', methods=['POST'])
        def calculate_distance():
            data = request.json
            point1 = data['point1']
            point2 = data['point2']
            distance = self.distance_metric(point1, point2)
            return jsonify({"distance": distance})

        app.run(host=host, port=port)





class AutomatedDistanceMetricSelection:
    def __init__(self, metrics=None):
        """
        Initialize the selector with a list of potential distance metrics.
        
        :param metrics: List of distance metric classes or functions to choose from.
        """
        if metrics is None:
            self.metrics = [
                Euclidean(),
                CosineSimilarity(),
                Manhattan(),
                Jaccard(),
                Mahalanobis(),
                DynamicTimeWarping(),
                Frechet(),
                # Add other metrics as needed
            ]
        else:
            self.metrics = metrics
    
    def select_metric(self, data):
        """
        Automatically select the best distance metric based on data characteristics.
        
        :param data: The data to analyze (e.g., a numpy array or pandas DataFrame).
        :return: The selected distance metric class/function.
        """
        # Example heuristic based on data characteristics
        if self.is_high_dimensional(data):
            return CosineSimilarity()
        elif self.is_binary_data(data):
            return Jaccard()
        elif self.has_outliers(data):
            return Manhattan()
        elif self.is_time_series(data):
            return DynamicTimeWarping()
        else:
            # Default choice if no specific conditions are met
            return Euclidean()

    def is_high_dimensional(self, data):
        """Heuristic: Check if the data is high-dimensional."""
        return data.shape[1] > 50

    def is_binary_data(self, data):
        """Heuristic: Check if the data consists of binary values."""
        return np.array_equal(data, data.astype(bool))

    def has_outliers(self, data):
        """Heuristic: Check if the data has significant outliers."""
        q1, q3 = np.percentile(data, [25, 75], axis=0)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return np.any((data < lower_bound) | (data > upper_bound))

    def is_time_series(self, data):
        """Heuristic: Check if the data is time-series data."""
        # Simple heuristic: time series often have more rows than columns
        return data.shape[0] > data.shape[1]


