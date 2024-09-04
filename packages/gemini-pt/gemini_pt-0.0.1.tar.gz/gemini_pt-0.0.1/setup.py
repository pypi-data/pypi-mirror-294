from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Automatic pentest using AI'
LONG_DESCRIPTION = 'This program use the Gemini API to perform the first steps of a pentest'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="gemini_pt", 
        version=VERSION,
        author="Elouan Teissere",
        author_email="<elouan.teissere@sii.fr>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'python-dotenv',
            'google-generativeai',
            'grpcio',
            'markdown2',
            'pdfkit',
            'openai',
            'python-nmap'
        ],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3.9",
            "Operating System :: MacOS :: MacOS X",],
        entry_points={
            'console_scripts': [
                'gemini_pt = gemini_pt.main:main',
            ],
        }
)