import setuptools
from codecs import open
import os

wip_version = "1.0.1"

def readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except IOError:
        return 'Not Found'

setuptools.setup(
    name="pl_build",
    version=wip_version,
    license='MIT',
    python_requires='>=3.6',
    author="Jonathan Hoffstadt",
    author_email="jonathanhoffstadt@yahoo.com",
    description='Pilot Light Build',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/PilotLightTech/pilotlight', # Optional
    packages=['pl_build'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={  # Optional
        'pl_build': ['README.md']
    }
)
