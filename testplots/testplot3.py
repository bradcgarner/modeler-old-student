import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(14, 7)) # width, height of canvas
ax = plt.subplot(111) # 111 = 1 rows, 1 columns, use column 1
                      # 432 = 4 rows, 3 columns, use column 2
ax.set_aspect('auto')   # 1 = height = 1*width; 'equal' does same as 1
                      # try decimal, e.g. height = 0.25 * width
                      # try 'auto'

time = np.arange(100)
rain = [0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1,0,0,0,1,2,3,7,9,0,1]
ret = [0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1,0,0,0,.5,1.2,2,3,4,3.4,3.1]

# plt.plot(np.arange(10)) # 10 evenly spaced numbers
# plt.plot([6,7,8,9],[2,8,5,4]) #x,y
# plt.plot([6,7,8,9],[3,7,6,5]) #x,y
plt.plot(time,rain) # x,y
plt.plot(time,ret) # x,y

plt.xlabel('this is a xlabel\n(with newlines!)')
plt.ylabel('this is vertical\ntest', multialignment='center')
# plt.text(2, 7, 'this is\nyet another test',
#          rotation=45,
#          horizontalalignment='center',
#          verticalalignment='top',
#          multialignment='center')

plt.grid(True)

plt.show()