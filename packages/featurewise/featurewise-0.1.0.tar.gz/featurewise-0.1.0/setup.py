from setuptools import setup, find_packages

setup(
    name='featurewise',  # The name of your package
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find your package
    install_requires=[  # Dependencies your package needs
        'streamlit',
        'streamlit-aggrid',
        'pandas',
        'Numpy',
    ],
    entry_points={
        'console_scripts': [
            'featurewise = featurewise.featurewise:main',  # Command to run your app
        ],
    },
    description='A Streamlit app for feature engineering',
    author='Your Name',
    author_email='ambilybiju2408@gmail.com',
    url='https://github.com/ambilynanjilath/project',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
