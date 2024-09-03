import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from .Beam import Beam
from typing import Union

class Propagator:
    def __init__(self,
                 beam: Union[np.ndarray, Beam],
                 **kwargs) -> None:
        """
        Initialize the Propagator class to simulate the propagation of a beam.

        Parameters:
        beam (Union[np.ndarray, Beam]): The input beam to be propagated. Can be an instance of the Beam class or a 2D numpy array.
        **kwargs: Additional keyword arguments including:
            - k (float): Wave number. Default is for a wavelength of 632.8 nm.
            - L (float): Size of the computational domain. Default is 15e-3.

        Raises:
        ValueError: If the beam is a numpy array and its shape is not NxN.
        """
        if isinstance(beam, Beam):
            self.beam = beam.Beam.Beam
            self.k = beam.k
            self.L = beam.L
            self.N = beam.N
        elif isinstance(beam, np.ndarray):
            self.beam = beam
            self.k = (2*np.pi/632.8e-9) if 'k' not in kwargs else kwargs['k']
            self.L = 15e-3 if 'L' not in kwargs else kwargs['L']

            self.N = beam.shape[0]
            if self.beam.shape[0] != self.beam.shape[1]:
                raise ValueError('The shape of the Beam matrix must be NxN')
        
        if self.N % 2 == 0:
            fx = np.arange(-self.N//2, self.N//2) * (np.pi/self.L)

        else:
            fx = np.linspace(-self.N/2, self.N/2, self.N) * (np.pi/self.L)

        self.kx, self.ky = np.meshgrid(fx, fx)

    def Transfer_Function(self, z):
        """
        Compute the transfer function for a given propagation distance z.

        Parameters:
        z (float): The propagation distance.

        Returns:
        np.ndarray: The transfer function as a 2D numpy array.
        """
        return np.exp(1j * z * np.sqrt(self.k ** 2 - (self.kx ** 2 + self.ky ** 2)))

    
    def propagate(self, zi, zn):
        """
        Propagate the beam over a distance using the transfer function method.

        Parameters:
        zi (float): The total distance to propagate the beam.
        zn (int): The number of propagation steps.

        Creates:
        self.prop_beam (np.ndarray): 3D numpy array containing the propagated beam at each step.
        """
        self.prop_beam = np.zeros((self.N, self.N, zn), dtype=np.complex64)
        self.prop_beam[:,:,0] = self.beam
        self.z = np.linspace(0,zi,zn)
        a0 = np.fft.fftshift(np.fft.fft2(self.prop_beam[:,:,0]))
        for i,z in enumerate(self.z[1:], 1):
            a1 =  a0 * self.Transfer_Function(z=z)
            self.prop_beam[:,:,i] = np.fft.ifft2(np.fft.ifftshift(a1))
    
    def plot(self):
        """
        Plot the propagated beam intensity along the z-axis.
        """
        plt.imshow(np.abs(self.prop_beam[:,self.N//2,:]) ** 2)
        plt.colorbar()
        plt.show()

    def plot_amplitude(self):
        """
        Plot the amplitude of the propagated beam at the final propagation step.
        """
        plt.imshow(np.abs(self.prop_beam[:,:,-1])**2, extent=[-self.L, self.L, -self.L, self.L])
        plt.show()


class StokesParameters:
    def __init__(self,
                 P1,
                 P2,
                 P3,
                 P4) -> None:
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4

        """
        Initialize the StokesParameters class to calculate and plot the polarization ellipse.

        Parameters:
        P1, P2, P3, P4 (float): The four power meassurement.

        Creates:
        self.angle (float): The orientation angle of the polarization ellipse.
        self.E0x (float): The semi-major axis of the polarization ellipse.
        self.E0y (float): The semi-minor axis of the polarization ellipse.
        self.total_polarization (float): The degree of total polarization.
        """

        s0 = P1 + P2
        s1 = (P1 - P2)/s0
        s2 = (2*P3 - s0)/s0
        s3 = (s0 - 2*P4)/s0

        self.angle = np.rad2deg(0.5 * np.arctan(s2/s1))
        print(self.angle)
        self.E0x = np.sqrt(0.5*(1 + s1))
        self.E0y = np.sqrt(0.5*(1 - s1))

        self.total_polarization = np.sqrt(s1 ** 2 + s2 ** 2 + s3 ** 2)

        if self.total_polarization > 0:
            raise ValueError('P1, P2, P3, P4 are not correct')
            exit()

        self.plot_polarization()

    def plot_polarization(self):
        """
        Plot the polarization ellipse based on the calculated Stokes parameters.
        """
        fig, ax = plt.subplots()
        ellipse = Ellipse(xy = (0,0), width = 2*self.E0x, height = 2*self.E0y, angle = self.angle,  edgecolor='r', facecolor='none')
        ax.add_patch(ellipse)
        ax.axhline(y=0, color='black', linestyle='-')
        ax.axvline(x=0, color='black', linestyle='-')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect('equal')
        ax.set_title(f'Polarization: {self.total_polarization}')

        plt.show()
