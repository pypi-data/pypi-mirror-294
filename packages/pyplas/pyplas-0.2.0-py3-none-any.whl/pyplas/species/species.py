#!/usr/bin/python3
from scipy import constants as const
import numpy as np


class species():
    def __init__(self, m=None, n=None, T=300, q=None, P=None):
        self.n = n
        self.m = m
        self._q = q
        self.ideal_gas(n, T, P)

    @property
    def q(self):
        return self._q

    @q.setter
    def q(self, new_value):
        self._q = new_value    
        
    def ideal_gas(self, n, T, P):
        if T and n and not P:
            self.n = n
            self.T = T
            self.P = n*const.k*T
        
        elif T and P and not n:
            self.T = T
            self.P = P
            self.n = P/(const.k*T)
            
        elif P and n and not T:
            self.P = P
            self.n = n
            self.T = P/(const.k*n)
            
        else:
            self.P = P
            self.n = n
            self.T = T
            
    def element_info(self, name):
        from mendeleev import element
        self.element = element(name)
        self.m = self.element.mass*const.u
        try:
            self.ionization_energy = self.element.ionenergies[int(round(self._q/const.e + 1, 0))]*const.eV     
        except:
            self.ionization_energy = None
            
    def get_vth(self):
        if self.T and self.m:
            return np.sqrt(8*const.k*self.T/(np.pi*self.m))
        else:
            return None
        

class electrons(species):
    def __init__(self, n=None, T=None):
        super().__init__(m=const.m_e, n=n, T=T, q=-const.e)


class ions(species):
    def __init__(self, element, n=None, T=300, P=None, q=const.e):
        super().__init__(n=n, T=T, P=P, q=q)

        if not q:
            self._q = const.e
        else:
            self._q = q
        self.element_info(element)
        self.ideal_gas(n, T, P)

    @property
    def q(self):
        return self._q

    @q.setter
    def q(self, new_value):
        self._q = new_value
        self.element_info(self.element.symbol)


class neutrals(species):
    def __init__(self, element, n=None, T=300, P=None):
        super().__init__(n=n, T=T, P=P, q=0)
        self.element_info(element)
        self.ideal_gas(n, T, P)
        
        