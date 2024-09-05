try:
    from setuptools import setup

    _has_setuptools = True
except ImportError:
    from distutils.core import setup


def check_dependencies():
    install_requires = []

    try:
        import numpy
    except ImportError:
        install_requires.append("numpy")
    try:
        import scipy
    except ImportError:
        install_requires.append("scipy")

    return install_requires


# Function to parse requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Filter out comments and empty lines
        return [line.strip() for line in lines if line and not line.startswith("#")]

if __name__ == "__main__":
    install_requires = check_dependencies()

    setup(
        name="signalytica",
        version="0.1.19",
        author="Edgar Lara",
        author_email="elara480@gmail.com",
        description="Feature extraction for time series and EEG signals",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        url="https://github.com/Edgar-La/signalytica",
        #packages=find_packages(),
        #package_dir={"": "src"},  # Tells setuptools that packages are inside the src/ directory
        #packages=find_packages(where="src"),  # Automatically find all packages inside src/
        packages=["signalytica"],
        install_requires=parse_requirements('requirements.txt'),
        #install_requires=install_requires,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
    )
