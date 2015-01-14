#!/usr/bin/env python

from distutils.core import setup

setup(name='timegrep',
      version='1.4',
      description='Perform a binary search through a log file to find a range of times and print the corresponding lines',
      author='Fabrice FACORAT',
      author_email='fabrice.facorat@gmail.com',
      url='https://github.com/linux-wizard',
      scripts = ["timegrep"],
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: System Administrators',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Utilities',
      'Topic :: System :: Systems Administration'
      ]
     )
