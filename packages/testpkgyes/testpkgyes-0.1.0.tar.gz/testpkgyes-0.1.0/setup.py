from setuptools import setup, find_packages

setup(
    name='testpkgyes',  # Required: Name of your package
    version='0.1.0',  # Required: Version of your package
    description='A simple example package',  # Optional: Short description of the package
    author='NetSec',  # Optional: Your name as the author
    author_email='testauthor@example.com',  # Optional: Your email as the author
    url='https://github.com/netsec/testpkgyes',  # Optional: URL of the package (e.g., GitHub)
    packages=find_packages(),  # Required: Automatically find and include your packages
    classifiers=[  # Optional: Categories for your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Optional: Minimum Python version required
)
