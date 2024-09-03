import numpy as np

class Beam:
    def __init__(self,
                 *args,
                 **kwargs) -> None:
        
        """
        Initialize a beam of a specified type.

        Parameters:
        *args: Additional positional arguments (not used).
        **kwargs: Keyword arguments that specify beam properties, including:
            - type (str): Type of the beam (e.g., 'InceGaussian', 'HermiteGaussian', 'LaguerreGaussian', 'Gaussian').
            - w0 (float): Beam waist at z = 0. Default is 4e-4.
            - k (float): Wave number. Default corresponds to a wavelength of 632.8 nm.
            - z (float): Propagation distance. Default is 0.
            - shape (int): Number of grid points in each dimension. Default is 501.
            - size (float): Size of the computational domain. Default is 15e-3.
            - p (int): Radial mode index (for InceGaussian or LaguerreGaussian). Default is 2.
            - m (int): Azimuthal mode index (for InceGaussian or LaguerreGaussian) or order of Hermite polynomial (for HermiteGaussian). Default is 2.
            - elipticity (float): Ellipticity parameter (for InceGaussian). Default is 2.
            - parity (int): Parity of the Ince-Gaussian mode. Default is 0.
            - n (int): Order of Hermite polynomial (for HermiteGaussian). Default is 2.
            - l (int): Azimuthal index (for LaguerreGaussian). Default is 2.

        Raises:
        ValueError: If the specified beam type is not recognized.
        """
        assert kwargs['type'] is not None, 'Beam type has to be specified'
        self.type = 'HermiteGaussian' if 'type' not in kwargs else kwargs['type']
        self.w0 = 4e-4 if 'w0' not in kwargs else kwargs['w0']
        self.k = (2*np.pi/632.8e-9) if 'k' not in kwargs else kwargs['k']
        self.z = 0 if 'z' not in kwargs else kwargs['z']
        self.N = 501 if 'shape' not in kwargs else kwargs['shape']
        self.L = 15e-3 if 'size' not in kwargs else kwargs['size']


        match self.type:

            case 'InceGaussian':
                self.p = 2 if 'p' not in kwargs else kwargs['p']
                self.m = 2 if 'm' not in kwargs else kwargs['m']
                self.e = 2 if 'elipticity' not in kwargs else kwargs['elipticity']
                self.parity = 0 if 'parity' not in kwargs else kwargs['parity']
                from .InceGauss import InceGaussian
                self.Beam = InceGaussian(L = self.L,
                                        N = self.N,
                                        parity = self.parity,
                                        p = self.p,
                                        m = self.m,
                                        e = self.e,
                                        w0 = self.w0,
                                        k = self.k,
                                        z = self.z)
            
            case 'HermiteGaussian':
                self.m = 2 if 'm' not in kwargs else kwargs['m']
                self.n = 2 if 'n' not in kwargs else kwargs['n']

                from .HermiteGauss import HermiteGaussian
                self.Beam = HermiteGaussian(L = self.L,
                                            size = self.N,
                                            n = self.n,
                                            m = self.m,
                                            w0 = self.w0,
                                            k = self.k,
                                            z = self.z)
            
            case 'LaguerreGaussian':
                self.p = 2 if 'p' not in kwargs else kwargs['p']           
                self.l = 2 if 'm' not in kwargs else kwargs['l']

                from .LaguerreGauss import LaguerreGaussian
                self.Beam = LaguerreGaussian(L = self.L,
                                            size = self.N,
                                            p = self.p,
                                            l = self.l,
                                            w0 = self.w0,
                                            k = self.k,
                                            z = self.z)
            
            case 'Gaussian':
                from .Gaussian import Gaussian
                self.Beam = Gaussian(L = self.L,
                                    N = self.N,
                                    w0= self.w0,
                                    k = self.k,
                                    z = self.z)

            
            case _:
                raise ValueError('Type not found')
        
    def plot_amplitude(self):
        """
        Plot the amplitude of the beam.
        """
        self.Beam.plot_amplitude()

    def plot_phase(self):
        """
        Plot the phase of the beam.
        """
        self.Beam.plot_phase()

    def Hologram(self, gamma:float, theta:float, save:bool = False):
        """
        Generate and optionally save a hologram of the beam.

        Parameters:
        gamma (float): The angle for the hologram projection.
        theta (float): The rotation angle for the hologram.
        save (bool): If True, save the hologram image. Default is False.
        """
        self.Beam.Hologam(save = save, gamma = gamma, theta = theta)


Ince = Beam(type = 'InceGaussian',
            size = 5e-3, 
            shape = 501,
            parity = 0,
            p = 2,
            m = 2,
            e = 2,            
            w0 = 1e-3, 
            k = (2*np.pi/632.8e-9),
            z = 0)