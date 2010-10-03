from setuptools import setup, find_packages
setup(
    name = "{{ project_name }}",
    version = "0.1",
    packages = find_packages(),
    author = "Vince Veselosky",
    author_email = "vince@control-escape.com",
    description = "",
    license = "MIT",
    url = "",
    # could also include long_description, download_url, classifiers, etc.

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'docutils>=0.3',
        'django>=1.2,<1.3',
        'django-staticfiles',
        'PIL',
        'python-dateutil',
        'pytz',
        'south>0.7',
    ],

    include_package_data=True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the package, too:
        '': ['*.msg'],
    },


)