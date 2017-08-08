# CHRONOS - Time control application

CHRONOS is a simple time control application that intends to facilitate the record and management of tasks for projects. It is an opensource project based on Django 10.1 and Python 3. It uses the Ace Responsive Admin Template - https://wrapbootstrap.com/theme/ace-responsive-admin-template-WB0B30DGR - Kudos for them =)

## Getting Started

Download all the files, extract them into a folder. Run pip3 install -r requirements.txt (if you prefer to use virtualenv, feel free to do so).
After installing all the required Python3 libraries, run python3 manage.py migrate to create the database. When the migration process finishes, use the python3 manage.py loaddata initial_data.json to load the initial data.
Afterwards you can run python3 manage.py runserver to run the server.

Access using localhost:8000. Default username is chronos and default password is 123.abc.


### Prerequisites

Python 3 is a requirement. After that just run pip3 install -r requirements.txt to install the remaining requirements:

argon2-cffi==16.3.0
astroid==1.4.9
cffi==1.10.0
Django==1.10.5
django-appconf==1.0.2
django-compressor==2.1.1
django-widget-tweaks==1.4.1
isort==4.2.5
lazy-object-proxy==1.2.2
mccabe==0.6.0
olefile==0.44
Pillow==4.2.1
pycparser==2.18
pylint==1.6.5
rcssmin==1.0.6
reportlab==3.4.0
rjsmin==1.0.12
six==1.10.0
Unipath==1.1
wrapt==1.10.8

## Built With

* [Ace Responsive Admin Template](https://wrapbootstrap.com/theme/ace-responsive-admin-template-WB0B30DGR) - The web template used
* [django](https://www.djangoproject.com/) - Powerful web framework
* [PyCharm CE](https://www.jetbrains.com/pycharm/download/) - The IDE

## Authors

* **Hélder Pestana** - *Initial work* - [hgpestana](https://github.com/hgpestana)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Hat tip to anyone who's code was used

