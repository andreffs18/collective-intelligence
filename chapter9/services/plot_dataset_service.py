from pylab import *


class PlotDatasetService:

    def __init__(self, dataset):
        """
        From list of MatchRows, plot into graph
        """
        self.dataset = dataset

    def call(self):
        xdm = [r.data[0] for r in self.dataset if r.match == 1]
        ydm = [r.data[1] for r in self.dataset if r.match == 1]
        xdn = [r.data[0] for r in self.dataset if r.match == 0]
        ydn = [r.data[1] for r in self.dataset if r.match == 0]

        plot(xdm, ydm, 'bo')
        plot(xdn, ydn, 'b+')
        show()