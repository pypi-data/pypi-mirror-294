import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_packages(package):
    """Retourne les dossiers où un fichier __init__.py est présent
    
    Paramètres
        package(Str): le dossier à parcourir

    Retourne
        liste(list): liste des dossiers
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]
        
setuptools.setup(
     name='archiverr_client',  
     version='1.0.2', 
     scripts=['archiverr'] ,
     author="Théo Hurlimann",
     author_email="theo.hrlmn@hes-so.ch",
     description="Archiver is a tool to archive, search and extract files and folders based on his md5 hash",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=get_packages("src"),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License",
         "Operating System :: POSIX :: Linux",
     ],
    install_requires=[
        "setuptools>=62",
        "blinker==1.8.2",
        "certifi==2024.6.2",
        "charset-normalizer==3.3.2",
        "click==8.1.7",
        "Flask==3.0.3",
        "idna==3.7",
        "itsdangerous==2.2.0",
        "Jinja2==3.1.4",
        "MarkupSafe==2.1.5",
        "numpy==2.0.1",
        "pandas==2.2.2",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "PyYAML==6.0.1",
        "requests==2.32.3",
        "six==1.16.0",
        "tabulate==0.9.0",
        "tzdata==2024.1",
        "urllib3==2.2.2",
        "websockets==12.0",
        "Werkzeug==3.0.3"
    ],
    python_requires='>=3.11.9',

 )