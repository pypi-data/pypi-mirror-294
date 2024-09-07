from setuptools import setup, find_packages

setup(
    name='localvolts_api',
    version='0.2',
    author='Ian Connor',
    author_email='ian@blissai.com',
    description='A Python wrapper for the LocalVolts API',
    url='https://github.com/iconnor/localvolts',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
