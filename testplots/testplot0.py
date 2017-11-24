# Data for plotting
t = np.arange(0.0, 2.0, 0.01) # start at 0, go through 2.0, step at 0.01

s = # vertical axis
fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()