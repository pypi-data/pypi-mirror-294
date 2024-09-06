from setuptools import setup


# List of requirements
with open('deps.txt','r') as f:
    requirements = f.read().splitlines()




setup(
    name='lusid_bundle',
    version='1.2.1',
    install_requires=requirements,
    description='lusid-bundle is a python package that makes it quick and easy to install all of the Lusid and Luminesce sdks and dependencies.',
    long_description=open('README.md').read(),
    include_package_data=True,  
    long_description_content_type='text/markdown',
    python_requires='>=3.12', # no-bump
    author='Orlando Calvo',
    author_email='orlando.calvo@finbourne.com',
    url='https://gitlab.com/orlando.calvo1/lusid-bundle',
    classifiers=[
        'Development Status :: 3 - Alpha', # no-bump
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12', # no-bump
    ],
)