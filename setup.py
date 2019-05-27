import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='adr-tools-python',  
     version='0.0.1',
     scripts=['adr-config', 'adr-new', 'adr-init'] ,
     author="Victor Sluiter",
     author_email="vsluiter@yahoo.com",
     description="A package to provide adr-tools to python",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         'argparse'
     ]
 )
