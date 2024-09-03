from setuptools import setup, find_packages


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
   name='OptiKit',
   version='0.1.1a11',
   description='A basic optics module',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Armando Martinez',
   author_email='ar.martinez.hdz@hotmail.com',
   url= 'https://github.com/ARMANDOMTZ05/OptiKit',
   packages= find_packages(),
   install_requires=['matplotlib', 'numpy', 'scipy', 'pillow'],
   keywords= 'numpy, optics, holography, slm, python3, wavefront shaping',
   classifiers= ['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.10'],
   python_requires='>=3.10',
   license = 'MIT License' 
)