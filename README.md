# Birla-MUN-2021
![License](https://img.shields.io/badge/license-MIT-green)
![Flask](https://img.shields.io/badge/Flask-2.0.1-blue)

Delegate management and default zoom renaming and breakout rooms arrangement for Birla MUN'21 at Birla Vidya Niketan, New Delhi

# Installation

In case you want to run a development server on your local machine, then follow the following steps.

### Get the repository

Clone the repository

```
git clone https://github.com/Pancham1603/birla-mun-2021.git

cd birla-mun-2021
```

### Installing Virtual Environment

Be sure to have python >=3.6 installed in your machine and added to `$PATH` for *nix and to `environment variables` in Windows. Next create a virtual environment by installing and using `virtualenv`

```
pip install virtualenv
```

And then create a virtual environment

```
virtualenv somerandomname
```

Finally, activate the env

```
source somerandomname/bin/activate #For mac os and linux

somerandomname\Scripts\activate #For Windows; use backslash
```

### Installing Requirements

Use pip to install all the modules and libraries required for medSCHED in the required.txt

```
pip install -r requirements.txt
```

### Run Flask Server

Before running make sure that port 5000 is free or you can use any other port by passing the `port number` in the run function. You can start the development server like so

```
python3 main.py # For unix

python main.py # For Windows
```

# Screenshots

![Client 1](static/images/bmun1.png)
Home

![Client 2](static/images/bmun2.png)
Registration

![Client 3](static/images/bmun3.png)
Dashboard

![Admin 1](static/images/bmun4.png)
Scheduling a Meeting

![Admin 2](static/images/admin1.png)
Participant management

![Admin 3](static/images/admin2.png)
Meeting Management
