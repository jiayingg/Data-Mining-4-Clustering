from math import sqrt
from numpy import mean
import sys
import json

# Distance bewteen 2 points
def distance(p1,p2):
    return sqrt(sum((p1-p2)**2 for p1,p2 in zip(p1,p2)))

# Initial centroid: as far as possible
def get_initial_centroid(points,k):
    # First centroid: first point in the dataset
    centroid=[points[0]]

    # For a given k, need extra k-1 centroids
    for i in range(0,k-1):
        dist=[]
        for point in points:
            if point not in centroid:
                # dist: Minimum distance to centroids represents this point
                dist.append([point,min(distance(point,p) for p in centroid)])
        for point_dist in dist:
            # If the Minimum distance is the largest among all points, add it to centroids
            if point_dist[1]==max([p[1] for p in dist]):
                centroid.append(point_dist[0])
                break
    return sorted(centroid)

# Assign points to clusters
def assign(ctr,points):
    # Initialize the clusters
    clusters={}
    for i in range(0,len(ctr)):
        clusters[i]=[]

    for point in points:
        for centroid in ctr:
            # For every point, assign it to the cluster of nearest centroid
            if distance(centroid,point)==min(distance(point,p) for p in ctr):
                clusters[ctr.index(centroid)].append(point)
                break

    # Sort each cluster
    for i in range(0,len(ctr)):
        clusters[i]=sorted(clusters[i])

    return clusters.values()

# Recompute centroids after all points are assigned
def get_centroid(clusters):
    centroid=[]
    for cluster in clusters:
        centroid.append([mean([cluster[i][j]for i in range(0,len(cluster))]) for j in range(0,len(cluster[0]))])
    return sorted(centroid)

# Cohesion of the clustering
def get_cohesion(clusters):
    dia=[]
    for cluster in clusters:
        # Diameter: max distance between points in a cluster
        dia.append(max(distance(p1,p2) for p1 in cluster for p2 in cluster))
    return mean(dia)

# K-means algorithm
def kmeans(data_points,k):
    # Initialization
    centroid=get_initial_centroid(data_points,k)
    clusters=[]
    # This is used to determine when should stop
    oldCentroids = None

    # After each iteration, check if new centroid == old centroid
    # If TRUE, stop
    while not oldCentroids == centroid:
        oldCentroids = centroid
        clusters=assign(centroid,data_points)
        centroid=get_centroid(clusters)

    cohesion=get_cohesion(clusters)

    return clusters,cohesion


if __name__ == '__main__':
    input_lines = open(sys.argv[1])
    k = int(sys.argv[2])
    data_points=[]

    for line in input_lines:
        record = json.loads(line)
        data_points.append(tuple(record))

    # K clusters produced by kmeans and cohesion of the clustering
    clusters,cohesion=kmeans(data_points,k)
    for cluster in clusters:
        print cluster
    print cohesion