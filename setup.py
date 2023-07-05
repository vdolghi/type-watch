import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='type-watch',                           
    packages=['type-watch'],                    
    version='0.1.0',                                
    license='MIT',                                 
    description='Tools for enforcing strict type checking on functions and class methods',
    long_description=long_description,              
    long_description_content_type="text/markdown",  
    author='Vlad Dolghi',
    author_email='dolghi.vlad@gmail.com',
    url='TBA', 
    project_urls = {                                
        "Bug Tracker": "TBA"
    },
    keywords=["pypi", "type-watch", "strict types","types","typing"], 
    classifiers=[                                   
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    
    download_url="TBA",
)