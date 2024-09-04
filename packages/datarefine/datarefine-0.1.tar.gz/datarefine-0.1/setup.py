from setuptools import setup, find_packages

setup(
    name='datarefine',
    version='0.1',
    description='A Streamlit app for data cleaning and visualization',
    author='Shahana Farvin',
    author_email='shahana50997@example.com',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly',
        'requests',  # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'datarefine=DataRefine.DataRefine:main',
        ],
    },
)
