from setuptools import setup, find_packages

setup(
    name='zerodhawrapper',
    version='1.1',
    packages=find_packages(),
    py_modules=['zd'],  # Include zd.py as a module
    include_package_data=True,
    install_requires=[
        'kiteconnect',
        'pandas',
        'furl',
        'nsetools',
        'prettytable',
        'pyotp',
        'webdriver_manager',
        'selenium'
    ],
    package_data={
        'zerodhawrapper': ['config.ini'],
    },
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here if needed
            # Example: 'script_name=supertrend_script.your_script:main_function'
        ],
    },
)