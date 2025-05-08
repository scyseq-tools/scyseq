import numpy as np
import scipy as sp
import numpy.linalg

# This has been optimized and reimplemented in discretize.py

def clustervar(data,it):
    """
    This program compute a clustering of the data, the méthode is inspired by the method of the singular values decomposition, show Carsten Allefeld and all: Mental as macrostates emerging from brain dynamics.

    :param it: number of iteration, number of cluster = 2^(number of iterations)

    :return: a list of length n=2^it, each items i of the outputlist contains every point who belongs at the cluster i 
    """

    data = np.array(data)
    data = data/float(np.linalg.norm(data))
    npoint= np.shape(data)[0]
    cluster = ['']*npoint
    ncluster = 1
    arraycluster = np.ndarray((npoint,1))

    subdata = data 
    
    #Analyse du premier subdata
    U,S,V = np.linalg.svd(subdata)
    subdata = np.dot(subdata,V)

    med = np.median(subdata[:,0])

    for i in range(npoint):
        if subdata[i,0] <= med:
            cluster[i] += '0'
        if subdata[i,0] > med:
            cluster[i] += '1'
            
    ncluster = ncluster*2


    while ncluster < pow(2,it):
        print (ncluster)
 
        for k in range(0,ncluster):

            #creation of  subdata, first subdata 
            subdata = list()
            for j in range(npoint):
                if (int(cluster[j],2) == k)&(len(cluster[j])==np.log2(ncluster)):
                   subdata.append((data[j],j))

            arraysubdata=np.ndarray((len(subdata),np.shape(data)[1]))
            for i in range(len(subdata)):
                 arraysubdata[i]=subdata[i][0]

            #analyze du subdata
            U,S,V = np.linalg.svd(arraysubdata)
            arraysubdata = np.dot(arraysubdata,V)
            med = np.median(arraysubdata[:,0])

            for i in range(len(subdata)):
                if arraysubdata[i][0] <= med:
                    cluster[subdata[i][1]] += '0'
                if arraysubdata[i][0] > med:
                    cluster[subdata[i][1]] += '1'
                 
        ncluster = ncluster*2

    



    #Organize the outputlist
    retcluster=list()
    totcluster=pow(2,it)
    for i in range(totcluster):
        retcluster.append('')
        retcluster[i]=list('')
        for k in range(npoint):
            if int(cluster[k],2)==i:
                retcluster[i].append(data[k])
        retcluster[i]=np.array(retcluster[i])
    
        
    return retcluster
