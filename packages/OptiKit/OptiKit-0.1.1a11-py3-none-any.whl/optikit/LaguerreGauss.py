import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial
from PIL import Image


def LP(n, alpha, x):
    """
    Calculate the generalized Laguerre polynomial.

    Parameters:
    n (int): The degree of the polynomial.
    alpha (float): The parameter α of the generalized Laguerre polynomial.
    x (float or array-like): The input value(s) where the polynomial is evaluated.

    Returns:
    np.ndarray or float: The evaluated Laguerre polynomial at x.
    """

    L_n_alpha = genlaguerre(n, alpha)(x)

    return L_n_alpha

class LaguerreGaussian:
    """
    A class to represent and generate Laguerre-Gaussian modes.

    The `LaguerreGaussian` class generates a Laguerre-Gaussian mode based on the specified parameters p and l.
    It also supports the generation of binary holograms tailored to Spatial Light Modulators (SLMs) with a resolution of 1920x1080.

    Attributes:
        L (float): The size of the computational domain.
        size (int): The number of grid points in each dimension.
        p (int): The radial mode index (p ≥ 0).
        l (int): The azimuthal mode index.
        w0 (float): The beam waist at z = 0.
        k (float): The wave number.
        z (float): The propagation distance.


    Methods:
        plot_amplitude():
            Plots the amplitude of the Hermite-Gaussian mode.
        plot_phase():
            Plots the phase of the Hermite-Gaussian mode.
        Hologram(gamma, theta, save=False):
            Generates and optionally saves a binary hologram.
    """
    def __init__(self,
                 L: float,
                 size: int,
                 p: int,
                 l: int,
                 w0: float,
                 k: float,
                 z: float) -> None:
        """
        Initialize the Laguerre-Gaussian Modes class.

        Parameters:
        L (float): The size of the computational domain.
        size (int): The number of grid points in each dimension.
        p (int): The radial mode index (p ≥ 0).
        l (int): The azimuthal mode index.
        w0 (float): The beam waist at z = 0.
        k (float): The wave number.
        z (float): The propagation distance.

        Raises:
        ValueError: If p is negative.
        """

        if p < 0:
            raise ValueError('p must be positive')
        
        self.size = size
        self.L = L
        self.w0 = w0
        self.p = p
        self.l = l
        self.k = k
        self.z = z


        x, y = np.linspace(-self.L, self.L, self.size), np.linspace(-self.L, self.L, self.size)
        self.Y, self.X = np.meshgrid(x, y)

        r = np.sqrt(self.X ** 2 + self.Y ** 2)
        theta = np.arctan2(self.Y,self.X)

        if self.z == 0:
            lgb = (1/self.w0) * (r*np.sqrt(2)/self.w0)**(np.abs(self.l)) * np.exp(-r**2/self.w0**2) * LP(self.p, np.abs(self.l), 2*r**2/self.w0**2) * np.exp(-1j*self.l*theta)

        else:
            zr = 1/2 * self.k * self.w0 ** 2
            wz = self.w0 * np.sqrt(1 + (z/zr) ** 2)
            Rz = z * (1 + (zr / z) ** 2)
            CMnumber = np.abs(self.l) + 2 * self.p

            self.GouyPhase = (CMnumber + 1) * np.arctan(z/zr)

            lgb = (1/wz) * (r*np.sqrt(2)/wz)**(np.abs(self.l)) * np.exp(-r**2/wz**2) * LP(self.p, np.abs(self.l), 2*r**2/wz**2) * np.exp(-1j*self.k*r**2/(2*Rz)) * np.exp(-1j*self.l*theta) * np.exp(1j * self.GouyPhase)

        Norm = np.sqrt((2*factorial(self.p))/(np.pi*factorial(self.p + np.abs(self.l))))

        self.Beam = lgb * Norm

    def plot_amplitude(self):
        """
        Plot the amplitude of the Hermite-Gaussian mode.

        This method visualizes the magnitude of the Hermite-Gaussian mode on a 2D grid.
        """
        plt.imshow(np.abs(self.Beam), extent=[-self.L, self.L, -self.L, self.L] , cmap= 'gray')
        plt.title(f'Laguerre-Gaussian Mode l = {self.l}, p = {self.p}, z = {self.z}')
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.show()

    def plot_phase(self):
        """
        Plot the phase of the Hermite-Gaussian mode.

        This method visualizes the phase of the Hermite-Gaussian mode on a 2D grid.
        """
        plt.imshow(np.angle(self.Beam) ,cmap= 'gray')
        plt.title(f'Phase Laguerre-Gaussian Mode l = {self.l}, p = {self.p}, z = {self.z}')
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.show()

    def Hologam(self, gamma, theta, save:bool = False):
        """
        Generate a binary hologram based on the Hermite-Gaussian mode.

        This method generates a binary hologram that can be used with a Digital Micromirror Device (DMD)
        or Spatial Light Modulator (SLM) of resolution 1920x1080.

        Parameters:
            gamma (float): The angle in radians that defines the off-axis tilt of the hologram.
            theta (float): The angle in radians that defines the azimuthal direction of the off-axis tilt.
            save (bool): If True, saves the generated hologram as 'LaguerreGauss.png'. Default is False.

        Returns:
            np.ndarray: The generated binary hologram as a 1920x1080 array.
        """
        self.kxy = self.k *np.sin(gamma)
        self.kx = self.kxy * np.cos(theta)
        self.ky = self.kxy * np.sin(theta)

        Hologram = np.zeros((1080, 1920), dtype= np.uint8)

        Beam = np.exp(1j* (self.kx * self.X + self.ky * self.Y)) * self.Beam

        Amp = np.abs(Beam)
        Amp = Amp/np.max(Amp)

        phi = np.angle(Beam)
        pp = np.arcsin(Amp)

        qq = phi

        CoGH = _insertImage(1 - (0.5 + 0.5 * np.sign(np.cos(pp) + np.cos(qq))), Hologram)

        if save:
            Image.fromarray(CoGH * 255).convert('1').save('LaguerreGauss.png')

        return np.round((2**8-1)* CoGH).astype('uint8')



def _insertImage(image,image_out):
    """
    Insert a smaller image into the center of a larger image array.

    Parameters:
        image (np.ndarray): The smaller image to be inserted.
        image_out (np.ndarray): The larger output image array.

    Returns:
        np.ndarray: The combined image with the smaller image inserted at the center.
    """
    N_v, N_u = image_out.shape

    S_u = image.shape[1]
    S_v = image.shape[0]
  
    u1, u2 = int(N_u/2 - S_u/2), int(N_u/2 + S_u/2)
    v1, v2 = int(N_v/2 - S_v/2), int( N_v/2 + S_v/2)

    if u1 < 0 or u2 > N_u:
        raise Exception("Image could not be inserted because it is either too large in the u-dimension or the offset causes it to extend out of the input screen size")
    if v1 < 0 or v2 > N_v:
        raise Exception("Image could not be inserted because it is either too large in the v-dimension or the offset causes it to extend out of the input screen size")
        
    image_out[v1:v2,u1:u2] = image


    return image_out

