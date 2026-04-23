    
import generator as G

a = G.generate('uniform', 500, 4)
b = G.generate('uniform', 500, 4)

rp = recurrence_plot((a,b))

import matplotlib.pyplot as plt
plt.matshow(rp, cmap=plt.get_cmap('binary'))

l = G.generate('binary_logistic', 500, 2, 4.) 
rpl = recurrence_plot((l,))
plt.matshow(rpl, cmap=plt.get_cmap('binary'))

l1 = G.generate('binary_logistic', 250, 2, 4.) 
l2 = G.generate('binary_logistic', 250, 2, 3.)
lbis = l1 + l2
rplbis = recurrence_plot((lbis,))
plt.matshow(rplbis, cmap=plt.get_cmap('binary'))

plt.show()
