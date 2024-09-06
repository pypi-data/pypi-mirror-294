from setuptools import setup, find_packages

setup(
    name='drcodecover',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'sentry-sdk>=2.0.0',  # Specify a version range for better compatibility
    ],
    author='Mohd Nadeem',
    author_email='codewithnadeem@gmail.com',
    description='A special package for Sentry integration with advanced configuration options.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/codewithnadeem14502/drcode-wrapper-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',  # Specify minimum Python version
    project_urls={  # Additional metadata
        'Documentation': 'https://github.com/codewithnadeem14502/drcode-wrapper-python#readme',
        'Source': 'https://github.com/codewithnadeem14502/drcode-wrapper-python',
    },
)
