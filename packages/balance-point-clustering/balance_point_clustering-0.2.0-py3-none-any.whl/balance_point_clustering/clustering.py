import numpy as np
import math
import pandas as pd

def balance_point_clustering(df, no_clusters="DYNAMIC"):
    """
    Perform balance point clustering on the given DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the features to be clustered.
    no_clusters (int or str): The desired number of clusters. If not defined, the algorithm will determine the optimal number of clusters.

    Returns:
    list: A list of clusters where each cluster is a list of points (tuples).
    """

    # Convert DataFrame to numpy array
    points = df.to_numpy()
    n, dimensions = points.shape

    dist = []
    sum_coords = np.zeros(dimensions)

    # Compute the sum of each coordinate across all points
    for point in points:
        sum_coords += point

    # Compute the centroid of all points
    centroid = sum_coords / n

    # Calculate the Euclidean distance of each point from the centroid
    for point in points:
        dist1 = np.sqrt(np.sum((centroid - point) ** 2))
        dist.append(dist1)

    # Sort distances and corresponding points
    sorted_indices = np.argsort(dist)
    dist = [dist[i] for i in sorted_indices]
    points = [tuple(points[i]) for i in sorted_indices]

    # Initialize cluster tables with infinity
    cluster_table = np.full((n, n), np.inf, dtype=float)
    cluster_points = [[[] for _ in range(n)] for _ in range(n)]

    # Assign the first point to the first cluster
    cluster_table[0][0] = dist[0]
    cluster_points[0][0] = points[0]

    i_ptr = 0
    j_ptr = 0
    actual_clusters = 1

    # Assign points to clusters based on distance comparison
    for i in range(1, n-1):
        pre = abs(dist[i] - dist[i-1])
        post = abs(dist[i] - dist[i+1])

        if pre < post:
            if j_ptr < n-1:
                j_ptr += 1
            else:
                actual_clusters += 1
                i_ptr += 1
                j_ptr = 0
            cluster_table[i_ptr][j_ptr] = dist[i]
            cluster_points[i_ptr][j_ptr] = points[i]
        else:
            actual_clusters += 1
            i_ptr += 1
            j_ptr = 0
            cluster_table[i_ptr][j_ptr] = dist[i]
            cluster_points[i_ptr][j_ptr] = points[i]

    # Add the last point to the clusters
    if j_ptr < n-1:
        j_ptr += 1
    else:
        i_ptr += 1
    cluster_table[i_ptr][j_ptr] = dist[-1]
    cluster_points[i_ptr][j_ptr] = points[-1]

    # If no_clusters is not defined, use the calculated dynamic number of clusters
    if no_clusters == "DYNAMIC":
        no_clusters = actual_clusters

    # Adjust clusters to match the desired number
    while actual_clusters > no_clusters:
        above = abs(cluster_table[i_ptr][0] - cluster_table[i_ptr-1][0])
        below = abs(cluster_table[i_ptr][0] - cluster_table[i_ptr+1][0])
        no_ele = sum(1 for val in cluster_table[i_ptr] if val != np.inf)

        if above <= below:
            j_ptr = next(j for j, val in enumerate(cluster_table[i_ptr-1]) if val == np.inf)
            cluster_table[i_ptr-1, j_ptr:j_ptr+no_ele] = cluster_table[i_ptr, :no_ele]
            cluster_points[i_ptr-1][j_ptr:j_ptr+no_ele] = cluster_points[i_ptr][:no_ele]
        else:
            j_ptr = next(j for j, val in enumerate(cluster_table[i_ptr+1]) if val == np.inf)
            cluster_table[i_ptr+1, j_ptr:j_ptr+no_ele] = cluster_table[i_ptr, :no_ele]
            cluster_points[i_ptr+1][j_ptr:j_ptr+no_ele] = cluster_points[i_ptr][:no_ele]

        cluster_table[i_ptr] = cluster_table[i_ptr+1]
        cluster_points[i_ptr] = cluster_points[i_ptr+1]
        i_ptr -= 1
        actual_clusters -= 1

    # Collect and return the final clusters
    clusters = []
    for i in range(no_clusters):
        cluster = [cluster_points[i][j] for j in range(n) if cluster_table[i][j] != np.inf]
        clusters.append(cluster)

    return clusters
