__author__ = 'Daan Wierstra and Tom Schaul'

from scipy import size, zeros, ndarray, array
from numpy.random import randn

from pybrain.structure.evolvables.evolvable import Evolvable


class ParameterContainer(Evolvable):
    """ A common interface implemented by all classes which
    contains data that can change during execution (i.e. trainable parameters)
    and should be losslessly storable and retrievable to files.  """
    
    # standard deviation for random values, and for mutation
    stdParams = 1.
    mutationStd = 0.1
    
    # if this variable is set, then only the owner can set the params or the derivs of the container
    owner = None
    
    # a flag that enables storage of derivatives
    hasDerivatives = False
    
    def __init__(self, paramdim = 0, **args):
        """ initialize all parameters with random values, normally distributed around 0
            @param stdParams: standard deviation of the values (default: 1). 
        """
        self.setArgs(**args)
        self.paramdim = paramdim
        if paramdim > 0:
            self._params = zeros(self.paramdim)
            # enable derivatives if it is a instance of Module or Connection
            # CHECKME: the import can not be global?
            from pybrain.structure.modules.module import Module
            from pybrain.structure.connections.connection import Connection
            if isinstance(self, Module) or isinstance(self, Connection):
                self.hasDerivatives = True
            if self.hasDerivatives:
                self._derivs = zeros(self.paramdim)
            self.randomize()
                   
    @property
    def params(self):
        """ @rtype: an array of numbers. """
        return self._params
    
    def __len__(self):
        return self.paramdim
    
    def _setParameters(self, p, owner = None):
        """ @param p: an array of numbers """
        assert self.owner == owner
        if isinstance(p, list):
            p = array(p)
        assert isinstance(p, ndarray)        
        self._params = p
        self.paramdim = size(self.params)
                
    @property
    def derivs(self):
        """ @rtype: an array of numbers. """
        return self._derivs
    
    def _setDerivatives(self, d, owner = None):
        """ @param d: an array of numbers of self.paramdim """
        assert self.owner == owner
        assert size(d) == self.paramdim
        self._derivs = d
    
    def resetDerivatives(self):
        """ @note: this method only sets the values to zero, it does not initialize the array. """
        assert self.hasDerivatives
        self._derivs *= 0
    
    def randomize(self):
        self._params[:] = randn(self.paramdim)*self.stdParams
        if self.hasDerivatives:
            self.resetDerivatives()
            
    def mutate(self):
        self._params += randn(self.paramdim)*self.mutationStd
            