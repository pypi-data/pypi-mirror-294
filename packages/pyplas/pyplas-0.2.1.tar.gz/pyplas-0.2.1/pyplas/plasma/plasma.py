#!/usr/bin/python3
from scipy import constants as const
import numpy as np
from ..species import ions as ion_species
from ..species import electrons as electron_species
from ..species import neutrals as neutral_species

class plasma():
    def __init__(self, electrons=None, ions=None, neutrals=None, 
                 potential=None, B=0):
        
        self.B = B
        self.potential = self.Phi = potential

        if ions:
            self.ions = ions
        else:
            self.ions = ion_species()
            
        if electrons:
            self.electrons = electrons
        else:
            self.electrons = electron_species()
            
        if neutrals:
            self.neutrals = neutrals
        else:
            self.neutrals = neutral_species()
            
        self.ion_neutral_cx = None
        self.ion_neutral_MFP = None
        self.ion_neutral_freq = None
        
    @property
    def Ti(self):
        return self.ions.T
    @Ti.setter
    def Ti(self, new_value):
        self.ions.T = new_value    
    @property
    def ni(self):
        return self.ions.n
    @ni.setter
    def ni(self, new_value):
        self.ions.n = new_value                
    @property
    def mi(self):
        return self.ions.m
    @mi.setter
    def mi(self, new_value):
        self.ions.m = new_value                

    @property
    def Te(self):
        return self.electrons.T
    @Te.setter
    def Te(self, new_value):
        self.electrons.T = new_value    
    @property
    def ne(self):
        return self.electrons.n
    @ne.setter
    def ne(self, new_value):
        self.electrons.n = new_value                
    @property
    def me(self):
        return self.electrons.m
    @me.setter
    def me(self, new_value):
        self.electrons.m = new_value             
        
    @property
    def Tg(self):
        return self.neutrals.T
    @Tg.setter
    def Tg(self, new_value):
        self.neutrals.T = new_value    
    @property
    def ng(self):
        return self.neutrals.n
    @ng.setter
    def ng(self, new_value):
        self.neutrals.n = new_value                
    @property
    def mg(self):
        return self.neutrals.m
    @mg.setter
    def mg(self, new_value):
        self.neutrals.m = new_value             

 
    def get_ion_neutral_MFP(self):
        return 1/(self.ng*self.ion_neutral_cx) # TODO check!
    
    def get_ion_neutral_freq(self):
        freq = self.ng * self.ion_neutral_cx \
                            * np.sqrt(8*const.k*self.Ti/(np.pi*self.mi))
        return freq
    
    def get_Bohm_speed(self):
        if self.Te and self.mi:
            return np.sqrt(const.k*self.Te/self.mi)
        else:
            print("Need electron temperature and ion mass for Bohm speed.")
            return None

    def get_Debye(self):
        return np.sqrt(const.epsilon_0*const.k*self.Te/(self.ne * const.e**2))
    
    def get_electron_gyro_radius(self):
        if self.B and self.electrons:
            return np.abs(self.me*self.electrons.get_vth()/(self.electrons.q * self.B))
        else:
            print("Need electron properties and magnetic field to calculate gyro radius.")
            return None

    def get_ion_gyro_radius(self):
        if self.B and self.ions:
            return np.abs(self.mi*self.ions.get_vth()/(self.ions.q * self.B))
        else:
            print("Need ion properties and magnetic field to calculate gyro radius.")
            return None

    def get_electron_gyro_freq(self):
        if self.B and self.electrons:
            return np.abs(self.electrons.q * self.B/self.me)
        else:
            print("Need electron properties and magnetic field to calculate gyro frequency.")
            return None

    def get_ion_gyro_freq(self):
        if self.B and self.ions:
            return np.abs(self.ions.q * self.B/self.mi)
        else:
            print("Need ion properties and magnetic field to calculate gyro frequency.")
            return None


