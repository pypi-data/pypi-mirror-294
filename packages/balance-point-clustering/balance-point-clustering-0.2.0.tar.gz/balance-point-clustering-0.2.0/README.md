# Balance Point Clustering

This package provides the Balance Point Clustering algorithm that can be used to cluster data points based on their Euclidean distance from their centroid which may also be known as the balance point of these data points. The facility of clustering the data to the number of clusters desired is given. The no. of clusters desired to be generated may be given as input along with the DataFrame in which the data points to be clustered are present. If there is an uncertainity or a good degree of freedom available in selecting the number of clusters for the data points used, the dynamic clustering feature available may be the optimal choice. All that needs to be done is to simply pass in the DataFrame that contains the data points upon which the clustering needs to be done, then the optimal number of clusters for that particular set of data points may be decided by the Balance Point Clustering algorithm itself. The number of clusters decided by the algorithm depends on the balance point of the given set of data points and the distribution of the data points around the balance point. 

## Installation

Install the package using pip:

```bash
pip install balance-point-clustering
