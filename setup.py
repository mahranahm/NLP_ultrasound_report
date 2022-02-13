from distutils.core import setup

# README file contents
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='NLP-ultrasound-report',
    version='0.1dev',
    packages=['src',],
    description='NLP Ultrasound Report Project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=['Ahmed Mahran', 'Cesare Spinoso-Di Piano'],
    author_email=['ahmed.mahran10@gmail.com', 'cesare.spinoso-dipiano@mail.mcgill.ca'],
    install_requires=[]
)