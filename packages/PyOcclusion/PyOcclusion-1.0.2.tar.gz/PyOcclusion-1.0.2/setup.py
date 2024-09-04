from setuptools import setup, find_packages

setup(
    name='PyOcclusion',
    version='1.0.2',
    packages=find_packages(where='PyOcclusion-Package/src'),
    package_dir={'': 'PyOcclusion-Package/src'},
    install_requires=[
        'numpy',
        'scikit-image',
        'imageio',
        'av',
        'Pillow>=10.0.1',
        'matplotlib',
    ],
    author='Bohdan Synytskyi',
    author_email='bodiasynytskiy@gmail.com',
    description='A package for video editing with occlusion noise',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BohdanSynytskyi/PyOcclusion',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
