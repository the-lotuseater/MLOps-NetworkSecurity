from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    Returns a list of requirements
    
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: List[str]
    '''
    requirements = []
    try:
        with open('../requirements.txt', 'r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip()
                if line and line!='-e .':
                    requirements.append(line)
            # requirements = [req.strip() for req in data if req.strip() and not req!='-e .']
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Abhishek Birhade',
    author_email='agbirhade1@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)