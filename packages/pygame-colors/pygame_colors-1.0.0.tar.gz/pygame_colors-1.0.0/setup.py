from setuptools import setup, find_packages

setup(
    name="pygame_colors",  # Name of the module
    version="1.0.0",  # Version
    description="A simple Pygame module for accessing predefined colors that will ease your scripting and save the time",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Basit Ahmad Ganie",
    author_email="basitahmed1412@gmail.com",
    url="https://github.com/basitganie/pygame_colors",  # Replace with your repository URL
        packages=find_packages(where="src"),  # This will find the package in the 'src' directory
    package_dir={"": "src"},  # Tell setuptools that packages are under the 'src' directory
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
    install_requires=[
        'pygame',  # Automatically install pygame if the user doesn't have it
    ],
)
