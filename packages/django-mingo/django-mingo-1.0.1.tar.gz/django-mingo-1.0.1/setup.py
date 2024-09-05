from setuptools import setup, find_packages

setup(
    name='django-mingo',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Customize your django admin panel.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rupam Dhara',
    author_email='thedevgenius83@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'Django>=4.0',  # adjust the version as needed
        # add any other dependencies here
    ],
)
