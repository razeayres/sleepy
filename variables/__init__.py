from basic_dendritic import initialize as bsd
from create_facets import initialize as crf
from terrain_attr import initialize as tra
from class_facets import initialize as clf
from lfp import initialize as lfp
from cti import initialize as cti
from postprocessing import initialize as postprocessing
from temp import initialize as tmp

class initialize(bsd, crf, tra, clf, lfp, cti, postprocessing, tmp):
    def __init__(self, e):
        self.e = e
        bsd.__init__(self, self.e)
        crf.__init__(self, self.e)
        tra.__init__(self, self.e)
        clf.__init__(self, self.e)
        lfp.__init__(self, self.e)
        cti.__init__(self, self.e)
        postprocessing.__init__(self, self.e)
        tmp.__init__(self, self.e)