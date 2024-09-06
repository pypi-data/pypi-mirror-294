from setuptools import setup, find_packages

setup(
    name='aiii_Javharbek',
    version='0.24',
    packages=find_packages(),
    install_requires=[
        'opencv-python==4.8.0.76',
        'numpy==1.25.2',
        'scipy==1.11.4',
        'matplotlib==3.7.1',
        'tensorflow==2.15.0',
        'imgaug==0.4.0',
        'scikit-learn==1.2.2',
        'shapely==2.0.5'
    ],
    author='Javharbek',
    author_email='jakharbek@gmail.com',
    description='AIII',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
