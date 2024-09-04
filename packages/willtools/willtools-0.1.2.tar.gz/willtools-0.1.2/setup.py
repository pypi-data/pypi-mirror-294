from setuptools import setup, find_packages

setup(
    name='willtools',
    version='0.1.2',
    author='Will',
    author_email='your.email@example.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/elonniu/willtools',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[  # Add your package dependencies here
        # 'numpy>=1.19',
        # 'pandas>=1.2',
    ],
)
