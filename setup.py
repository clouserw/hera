from setuptools import setup

setup(
    name='hera',
    version='0.1',
    description='An interface to interact with a Zeus Traffic Manager.',
    long_description=open('README.rst').read(),
    author='Wil Clouser',
    author_email='wclouser@mozilla.com',
    url='http://github.com/clouserw/hera',
    license='BSD',
    packages=['hera'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
