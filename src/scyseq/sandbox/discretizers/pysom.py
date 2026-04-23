import numpy as np
import scipy as sp
import scipy.spatial
import scipy.linalg.basic



def som(data='', ncluster='',it=2):


    """
This program compute the Self Organizng Map, a clustering algorithm based on the Kohonen Network

    """

    data   = np.array(data)
    dim = np.shape(data)[1] # number of columns
    length = np.shape(data)[0]  # number of lignes
    alpha  = np.array(range(length,-1,-1))/float(length)
    sigma =alpha
    
    #generate random clusters
    cluster = np.array([[0.]*dim]*ncluster)
     
    for i in range(ncluster):
             cluster[i,:] = np.random.random(dim)
             

    for q in range(1,it):# compute the iteration of the algorithm


        #find the nearest cluster for each point of the data
        Tree = sp.spatial.KDTree(cluster)

        for j in range(length):
            dist,indice = Tree.query(data[j,:]) # distance to the nearest cluster and indice of the nerearest cluster in the cluster matrix
            nearestcluster=cluster[indice,:]

            # moving all the cluster

            for k in range(ncluster):  
              
                distcluster = sp.linalg.basic.norm(cluster[indice]-cluster[k]) #compute the distance between the nearest cluster end the cluster k
                cluster[k,:] += alpha[i]*np.exp(- (distcluster*distcluster)/float(2.*sigma[j]*sigma[j]) )*(data[j,:]-cluster[k,:])
    return cluster

  


     
         


     
   
