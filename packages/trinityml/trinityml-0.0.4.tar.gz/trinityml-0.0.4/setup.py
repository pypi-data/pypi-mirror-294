from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='trinityml',
    version='0.0.4',
    description='A Python SDK for record the LLM Experiment Execution', 
    author='Team Giggso',
    author_email='support@giggso.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roosterhr/gg_python_sdk',
    requires=['langfuse'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)


