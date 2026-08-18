from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    A function that will return all the requirements
    """
    requirements_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            ## Read Lines From A File
            lines = file.readlines()
            ## Read Each Line from a file
            for line in lines:
                requirement = line.strip()
                ## Ignore empty lines and -e
                if requirement and requirement != '-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("File not found")

    return requirements_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Aphiwe Shabalala",
    author_email="Shabalalaaphiwe64@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)