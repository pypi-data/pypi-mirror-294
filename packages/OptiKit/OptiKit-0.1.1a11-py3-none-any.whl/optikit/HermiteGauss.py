import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial, hermite
from PIL import Image

def HP(n, x):
    """
    Generate the Hermite polynomial H_n(x) using the Rodrigues formula.

    Parameters:
    n (int): The degree of the Hermite polynomial.
    x (float or np.ndarray): The point(s) at which to evaluate the polynomial.

    Returns:
    H_n_x (float or np.ndarray): The value(s) of the Hermite polynomial H_n(x).
    """
    p_monic = hermite(n)
    H_n_x = p_monic(x)

    return H_n_x

class HermiteGaussian:
    """
    A class to represent and generate Hermite-Gaussian modes.

    The `HermiteGaussian` class generates a Hermite-Gaussian mode based on the specified parameters n and m.
    It also supports the generation of binary holograms tailored to Spatial Light Modulators (SLMs) with a resolution of 1920x1080.

    Attributes:
        size (int): The grid size for the generated mode.
        L (int): The physical dimension (in meters) of the grid.
        w0 (float): The beam waist radius at z = 0.
        n (int): The order of the Hermite polynomial in the x-direction.
        m (int): The order of the Hermite polynomial in the y-direction.
        k (float): The wavenumber of the beam.
        z (float): The propagation distance along the z-axis.
        Beam (np.ndarray): The computed Hermite-Gaussian beam (complex field).
        GouyPhase (float): The Gouy phase shift (computed if z ≠ 0).

    Methods:
        plot_amplitude():
            Plots the amplitude of the Hermite-Gaussian mode.
        plot_phase():
            Plots the phase of the Hermite-Gaussian mode.
        Hologram(gamma, theta, save=False):
            Generates and optionally saves a binary hologram.
    """
    def __init__(self,
                L:int,
                size: int, 
                n:int,
                m: int,
                w0: float,
                k: float,
                z:float) -> None:
        self.size = size
        self.L = L
        self.w0 = w0
        self.n = n
        self.m = m
        self.k = k
        self.z = z

        """
        Initialize the HermiteGaussian class with the given parameters.

        Parameters:
            L (int): The physical dimension (in meters) of the grid.
            size (int): The grid size for the generated mode.
            n (int): The order of the Hermite polynomial in the x-direction.
            m (int): The order of the Hermite polynomial in the y-direction.
            w0 (float): The beam waist radius at z = 0.
            k (float): The wavenumber of the beam.
            z (float): The propagation distance along the z-axis.
        """

        x, y = np.linspace(-self.L, self.L, self.size), np.linspace(-self.L, self.L, self.size)
        self.Y, self.X = np.meshgrid(x, y)

        if self.z == 0:
            self.Beam = (1/self.w0) * np.sqrt(2/(np.pi * (2 ** (self.m+self.n)) * factorial(self.m) * factorial(self.n))) * HP(self.m, np.sqrt(2)*self.X/self.w0) * HP(self.n, np.sqrt(2)*self.Y/self.w0) * np.exp(-(self.X**2 + self.Y **2)/self.w0**2)

        else:

            zr = 1/2 * self.k * self.w0 ** 2
            wz = self.w0 * np.sqrt(1 + (z/zr) ** 2)
            Rz = z * (1 + (zr / z) ** 2)

            self.GouyPhase = np.arctan(z/zr)

            self.Beam = (1/wz) * np.sqrt(2/(np.pi * 2 ** (self.m+self.n) * factorial(self.m) * factorial(self.n))) * HP(self.m, np.sqrt(2)*self.X/wz) * HP(self.n, np.sqrt(2)*self.Y/wz)*np.exp(-(self.X**2 + self.Y **2)/wz**2) * np.exp(-1j * (self.k * self.z + (self.m + self.n + 1)*self.GouyPhase - self.k*(self.X**2 + self.Y**2)/(2*Rz)))


    def plot_amplitude(self):
        """
        Plot the amplitude of the Hermite-Gaussian mode.

        This method visualizes the magnitude of the Hermite-Gaussian mode on a 2D grid.
        """
        plt.imshow(np.abs(self.Beam), extent=[-self.L, self.L, -self.L, self.L] , cmap= 'gray')
        plt.title(f'Hermite-Gaussian Mode m={self.m}, n = {self.n}, z = {self.z}')
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.show()

    def plot_phase(self):
        """
        Plot the phase of the Hermite-Gaussian mode.

        This method visualizes the phase of the Hermite-Gaussian mode on a 2D grid.
        """
        plt.imshow(np.angle(self.Beam) ,cmap= 'gray')
        plt.title(f'Phase Hermite-Gaussian Mode m={self.m}, n = {self.n}, z = {self.z}')
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
            save (bool): If True, saves the generated hologram as 'HermGauss.png'. Default is False.

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
            Image.fromarray(CoGH * 255).convert('1').save('HermGauss.png')

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
