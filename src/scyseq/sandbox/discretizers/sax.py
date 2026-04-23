import numpy as np
import scipy as sp
import scipy.special


def norm(data):

    data = data/np.sqrt(np.var(data))
    data = data- np.mean(data)

    return data



def paa(data,nbin):

    """
    Compute the Picewise Aggregate Approximation of the data

    :param data: array like 
    :param nbin: length of the output vector (length/nbin is not necessary a integers)
    :return: array like, the PAA of the data

    This method is based on the code of Li Wei: http://alumni.cs.ucr.edu/~wli/
    """
  
    data = np.array(data)
    length = data.shape[0]
    bitperbin=float(length)/nbin
    intbin=length/nbin
    paa=np.zeros(nbin)
    


    r=float(0)
    tot=1
    for k in range(0,nbin):
        i=1
        r=float(1-r)
        paa[k] += data[intbin*k]*r
        tot=float(r)  
        r =  ((float(length)/nbin)-r) - (int(float(length)/nbin-r))
        

        while tot <= float(length)/nbin-1 :
            paa[k] += data[intbin*k + i]
            i   += 1
            tot +=1

        if intbin*k+i < length:
            paa[k] +=data[intbin*k+i]*r 
 
    paa=paa/bitperbin
 

    
    return paa

           




def sax(data,outputlength,nsymbol):

    """
Compute the SAX algorithm

    :param outputlength: length of the output vector
    :param nsymbol: size of the alphabet for thr output vector

    This method is based on:
        SAX a novel Symboli Representation of Time Series
        J.LIN and al.

    """



    # Find the breakpoint who divided the gaussian into equiprobable segment
    nbreakpoint =nsymbol-1
    breakpoint = np.array(np.zeros(nbreakpoint))
  
    if nsymbol%2 == 0:  
        
        
        breakpoint[nbreakpoint/2]=0.5

        for i in range(1,nbreakpoint/2+1):
            breakpoint[nbreakpoint/2+i] = + 0.5+i*1./nsymbol
            breakpoint[nbreakpoint/2-i] = 1-breakpoint[nbreakpoint/2+i]

        breakpoint = np.sqrt(2)*sp.special.erfinv(2*breakpoint-1) # Compute the inverse of the repartitions functions



    if nsymbol%2 == 1:

        for i in range(0,nsymbol/2):

            breakpoint[nsymbol/2+i] = 0.5 + 1./(2*nsymbol) + i*1./nsymbol
            breakpoint[nsymbol/2-1-i] = 1 -breakpoint[nsymbol/2 + i]

         
        breakpoint = np.sqrt(2)*sp.special.erfinv(2*breakpoint-1) # Compute the inverse of the repartitions functions

        #print breakpoint


    #Assign the symbol
    data = norm(data)
    datapaa = paa(data,outputlength)
    saxdata = np.array(np.zeros(outputlength))
   
    for i in range(outputlength):

        if datapaa[i] < breakpoint[0]:
            saxdata[i] = 0

        if datapaa[i] >= breakpoint[nbreakpoint-1]:
            saxdata[i] = nbreakpoint



        for j in range(0,nbreakpoint-1):
              if (breakpoint[j] <= datapaa[i] < breakpoint[j+1])== True:
                saxdata[i]=j+1             


    return saxdata
