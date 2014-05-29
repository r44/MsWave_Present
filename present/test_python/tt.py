import numpy as np
import matplotlib as ma
ma.use('Agg')
import matplotlib.pyplot as plt


data = np.random.rand(4,4)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(data,interpolation='none')

fig.savefig('test.eps')
fig.savefig('test.pdf')
fig.savefig('test.png')
