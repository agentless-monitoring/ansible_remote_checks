from setuptools import setup, find_packages

setup(
  name='ansible_remote_checks',
  version='0.1.2',
  description='Library for Nagios checks on linux systems',
  author='Alexander Lex, David Voit, Christian Zuegner',
  author_email='Alexander.Lex@osram-os.com, David.Voit@osram-os.com, Christian.Zuegner@osram-os.com',

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: System :: Monitoring',
    'Programming Language :: Python :: 2',
  ],

  install_requires=[
    'ansible'
    'argparse',
   ],

  packages=find_packages('src'),
  package_dir={'':'src'},

  scripts=[
    'nagios_checks/check_cpu_ansible',
    'nagios_checks/check_file_ansible',
    'nagios_checks/check_fs_ansible',
    'nagios_checks/check_memory_ansible',
    'nagios_checks/check_service_ansible',
    'nagios_checks/check_update_ansible',
    'nagios_checks/check_swap_ansible',
    'nagios_checks/check_load_ansible',
    'nagios_checks/check_sg_ansible',
    'nagios_checks/check_process_ansible',
    'nagios_checks/check_directory_ansible'
  ]
)

