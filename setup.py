from setuptools import setup, find_packages

setup(
    name="probe",
    version="0.1",
    packages=find_packages(),
    install_requires=["pygal>=1.7.0", "xlrd>=0.7.4", "xlwt>=1.0.0"],
    author="K. Vitanov",
    description="This limited statistical package",
    license="GNU",
    keywords="statistics",
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: End Users/Desktop',
      'Programming Language :: Python',
    ],

)
