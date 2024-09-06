from setuptools import setup, find_packages

setup(
    name='corerec',
    version='0.1.2',
    description='A Framework to built custom recommendation envornments.',
    author='Vishesh Yadav',
    author_email='sciencely98@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib==3.7.5',
        'networkx==3.1',
        'scikit_learn==1.3.2',
        'torch==2.3.0',
        'tqdm==4.64.1',
        'memory_profiler==0.57.0',
        'pandas',
        'torch_geometric',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)