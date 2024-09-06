from setuptools import setup, find_packages

setup(
    name='fpefs',
    version='0.1',
    description='A Python library for Feature Probability Estimation and Feature Selection.',
    author='Nehal Varma',
    author_email='nehalvarma85@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.18',
        'scikit-learn>=0.24'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
