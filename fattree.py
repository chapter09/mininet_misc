__author__ = 'chapter09'


"""
a fat tree implementation within the mininet envrionment

"""

from mininet.topo import Topo

class FatTree(Topo):
    "Create a fat-tree topology."

    def __init__(self, k=4):
        '''Init.

        @param k number of ports

        '''
        if (k % 2) != 0 or k <= 0:
            print "ERROR: k should be even number"
            exit(0)

        # Initialize topology
        Topo.__init__(self)

        self.coreSwitches = []
        self.pods = []

        #core
        for i in range(0, (k/2)**2):
            self.coreSwitches.append(self.addSwitch("cs_" + str(i)))
        
        for i in range(0, k):
            pod = self.__createPod(str(i), k)
            self.pods.append(pod)

        #aggreagate <--> core
        for pod in range(0, len(self.pods)):
            for aggr in range(0, len(self.pods[pod][0])):
                aggrSwitch = self.pods[pod][0][aggr]
                for core in range(aggr*k/2, (aggr+1)*k/2):
                    self.addLink(self.coreSwitches[core], aggrSwitch)

    def __createPod(self, podId, k):
        aggrSwitches = []
        torSwitches = []
        hosts = []

        #aggregate and tor
        for i in range(0, k/2):
            aggrSwitches.append(self.addSwitch("as_" + podId \
                    + "_" + str(i)))
            torSwitches.append(self.addSwitch("ts_" + podId \
                    + "_" + str(i)))

        #tor <--> aggregate
        for tor in range(0, len(torSwitches)):
            for aggr in range(0, len(aggrSwitches)):
                self.addLink(torSwitches[tor], aggrSwitches[aggr])
        
        #host <--> tor
        for tor in range(0, len(torSwitches)):
           for host in range(tor*k/2, (tor+1)*k/2):
               h = self.addHost("h_" + podId + \
                   "_" + str(host))
               hosts.append(h)
               self.addLink(torSwitches[tor], h)
        
        return (aggrSwitches, torSwitches, hosts) 

#class FatTreePod(Topo):
#    "Create a pod in a fat-tree"

#    def __init__(self, podId, k):
#        Topo.__init__(self)

#        self.podId = podId 
#        self.aggrSwitches = []
#        self.torSwitches = []
#        self.hosts = []

#        #aggregate and tor
#        for i in range(0, k/2):
#            self.aggrSwitches.append(self.addSwitch("as_" + podId + str(i)))
#            self.torSwitches.append(self.addSwitch("ts_" + podId + str(i)))

#        #tor <--> aggregate
#        for tor in range(0, len(self.torSwitches)):
#            for aggr in range(0, len(self.aggrSwitches)):
#                self.addLink(self.torSwitches[tor], self.aggrSwitches[aggr])
        
#        #host <--> tor
#            #for tor in range(0, len(self.torSwitches)):
#            #    for host in range(tor*k/2, (tor+1)*k/2):
#            #        h = self.addHost("h_" + podId + "_" + str(tor))
#            #        self.hosts.append(h)
#            #        self.addLink(tor, h)

topos = {'fattree': (lambda k: FatTree(k))}
