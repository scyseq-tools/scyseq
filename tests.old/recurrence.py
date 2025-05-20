import scikits.symbolic3.generator as G
import scikits.symbolic3.recurrence as R
import numpy as np

a = G.generate('uniform', 10, 4)
b = G.generate('uniform', 10, 4)

rp = R.recurrence(a) #,b))
# rp = np.array([[1,0,1],[0,1,0],[1,0,1]])
# print(R.diagonal_distribution(rp))
print(R.recurrence_rate(rp))

import matplotlib.pyplot as plt
plt.matshow(rp, cmap=plt.get_cmap('binary'))

#l = G.generate('binary_logistic', 500, 2, 4.) 
#rpl = R.recurrence(l) #,))
#plt.matshow(rpl, cmap=plt.get_cmap('binary'))
#
#l1 = G.generate('binary_logistic', 250, 2, 4.) 
#l2 = G.generate('binary_logistic', 250, 2, 3.)
#lbis = l1 + l2
#rplbis = R.recurrence((lbis,))
#plt.matshow(rplbis, cmap=plt.get_cmap('binary'))

plt.show()

