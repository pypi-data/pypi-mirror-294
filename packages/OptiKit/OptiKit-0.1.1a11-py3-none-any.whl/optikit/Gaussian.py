import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Gaussian:
    """
    A class to represent and generate a Gaussian beam.

    The `Gaussian` class generates a Gaussian beam profile based on specified beam parameters.
    It supports visualization of the amplitude and phase of the beam, as well as generating binary holograms
    suitable for Spatial Light Modulators (SLMs) with a resolution of 1920x1080.

    Attributes:
        L (float): The physical dimension (in meters) of the grid.
        N (int): The grid size for the generated beam.
        w0 (float): The beam waist radius at z = 0.
        z (float): The propagation distance along the z-axis.
        k (float): The wavenumber of the beam.
        Beam (np.ndarray): The computed Gaussian beam (complex field).

    Methods:
        plot_amplitude():
            Plots the amplitude of the Gaussian beam.
        plot_phase():
            Plots the phase of the Gaussian beam.
        Hologram(gamma, theta, save=False):
            Generates and optionally saves a binary hologram.
    """
    def __init__(self, L:float,
                 N:int,
                 w0:float,
                 z:float,
                 k:float) -> None:
        """
        Initialize the Gaussian class with the given parameters.

        Parameters:
            L (float): The physical dimension (in meters) of the grid.
            N (int): The grid size for the generated beam.
            w0 (float): The beam waist radius at z = 0.
            z (float): The propagation distance along the z-axis.
            k (float): The wavenumber of the beam.
        """
        self.L = L
        self.z = z
        self.N = N
        self.k = k
        self.w0 = w0

        x = np.linspace(-self.L, self.L, self.N)
        self.X, self.Y = np.meshgrid(x,x)
        r = np.sqrt(self.X**2 + self.Y**2)
        if self.z == 0:
                self.Beam = np.exp(-(r/self.w0)**2)

        else:
            zr = 1/2 * self.k * self.w0 ** 2
            wz = self.w0 * np.sqrt(1 + (self.z/zr))

            Rz = self.z * (1 + (zr/self.z) ** 2)
                
            G_pahse = np.arctan(self.z / zr)

            self.Beam = self.w0/wz * np.exp(-(r**2)/wz ** 2) * np.exp(-1j * (self.k*self.z + self.k * (r**2)/(2*Rz) - G_pahse))

    def plot_amplitude(self):
        plt.imshow(np.abs(self.Beam), extent=[-self.L, self.L, -self.L, self.L] ,cmap= 'gray')
        plt.title(f'Gaussian Mode z={self.z}')
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.show()

    def plot_phase(self):
        plt.imshow(np.angle(self.Beam) ,cmap= 'gray')
        plt.title(f'Phase Gaussian Mode z = {self.z}')
        plt.colorbar()
        plt.xlabel('x(m)')
        plt.ylabel('y(m)')
        plt.show()

    def Hologam(self, gamma, theta, save:bool = False):
        """
        Generate a binary hologram based on the Gaussian beam.

        This method generates a binary hologram that can be used with a Digital Micromirror Device (DMD)
        or Spatial Light Modulator (SLM) of resolution 1920x1080.

        Parameters:
            gamma (float): The angle in radians that defines the off-axis tilt of the hologram.
            theta (float): The angle in radians that defines the azimuthal direction of the off-axis tilt.
            save (bool): If True, saves the generated hologram as 'Gauss.png'. Default is False.

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
            Image.fromarray(CoGH * 255).convert('1').save('Gauss.png')

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