def graphIt(self):
    filename = self.surfaceName + 'Graph.png'
    plt.figure(figsize=(14, 7)) # width, height of canvas
    ax = plt.subplot(111) 
    ax.set_aspect('auto')  
    legendInfo = mpatches.Patch(color='white', label=self.surfaceName) 
    plt.legend(handles=[legendInfo])

    time = np.arange(len(self.rainList))

    # pass thru data now, later might aggregate into fewer points
    rain =         self.rainList
    uncontrolled = self.uncontrolledList
    controlled =   self.controlledList
    runoff =       self.runoffList
    et =           self.etList
    ret =          self.retList

    plt.plot(time,rain, 'k--',label='rain') # x,y
    plt.plot(time,uncontrolled)
    plt.plot(time,controlled)
    plt.plot(time,runoff)
    plt.plot(time,et)
    plt.plot(time,ret)

    plt.xlabel('time')
    plt.ylabel('volume', multialignment='center')
    plt.grid(True)

    plt.savefig(filename)