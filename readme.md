# Geek.Zone Web App
This application is currently intended as the minimum viable product for Geek.Zone members and n00bs to be able to manage their Geek.Zone membership. We will build it from there, but that's our target right now! We currently use a third party to do this, and while they are not a bad service per se, they do charge us for their services and do not do all the things we need them to do. Building it ourselves will not only mean that we get the system that we need, but also that those involved will learn new, transferrable skills and have some fun doing so.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

## Running the project locally

You should be able to setup this project on any operating system that supports Django. We have instructions for Ubuntu based linux distributions which can be found below; Windows instructions are in the pipeline.

### Ubuntu based Linux

> This guide assumes that you can execute basic terminal commands. It also assumes that you have setup github with SSH keys.

Ubuntu 20.04 and above should come with a recent enough version of python 3 for you to follow along with this guide. As of writing I am using python 3.8.5.

First follow the instructions below for initial setup.

1. Install the python package manager `pip` by running the command `sudo apt install python3-pip`
2. Install virtualenv using the command `python3 -m pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
3. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
4. Create a virtual environment `python3 -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
5. Activate the virtual environment `source env/bin/activate`.
6. Install the project dependencies `pip install -r requirements.txt`
7. Create the local database by running the migrations `python manage.py migrate`
8. Run the local server `python manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

The above instructions should be enough to get the django server running, and the membership management software accessible from a browser. There is a small amount of additional configuration required for a fully working system, which is OS agnostic. We will be producing a guide for this additional configuration soon.

After you have done the above subsequent setup is a lot simpler.
```sh
source env/bin/activate # You only need to do this if your virtual env is not already active
python manage.py runserver
```

If there are new changes to the database the runserver output will run you through the process of updating and running the migrations.

### Microsoft Windows (Without WSL)

> The following steps have only been tried on Windows 10 Pro in a virtual machine

1. Install git for windows by downloading a copy from https://git-scm.com/download/win
2. Install python from the Microsoft store. Typing `python` into a command prompt will open the correct page on the Microsoft store. This will also install the `pip` package manager.
3. Install virtualenv using the command `pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
4. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
4. Create a virtual environment `python3 -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
5. Activate the virtual environment `env\Scripts\activate.bat`
6. Install the project dependencies `pip install -r requirements.txt`
7. Create the local database by running the migrations `python manage.py migrate`
8. Run the local server `python manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

The above instructions should be enough to get the django server running, and the membership management software accessible from a browser. There is a small amount of additional configuration required for a fully working system, which is OS agnostic. We will be producing a guide for this additional configuration soon.

### Suggestions

Clearly, you can and should use which ever development tools you prefer. If you don't have a preference, we suggest trying,

#### Python
 * [PyCharm](https://www.jetbrains.com/pycharm/)
 * [Visual Studio Code](https://code.visualstudio.com/)
#### SQL
 * [DBeaver Community Edition](https://dbeaver.io/)
#### Diagrams
 * [DrawIO Desktop](https://github.com/jgraph/drawio-desktop/releases/tag/v13.3.1)

Also, do join us on our [Discord](https://geek.zone/discord)!

## Local Development

### Running the Tests

Simply run `python manage.py test`.

### Changing the CircleCI Build

We have found the [circleci local cli tool](https://circleci.com/docs/2.0/local-cli/) to be very useful when making changes to the circle build locally. The errors can be a bit cryptic, but it's easier than debugging basic syntax issues from within the circleci console.

## Contributing

Before you ask, we use [spaces](https://www.youtube.com/watch?v=SsoOG6ZeyUI).

Otherwise, no special rules, just pull request before merging, you know the drill ;) Little and often commits are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Geek.Zone members are invited to the Geek.Zone org on GitHub so that they can contribute directly. Membership only costs £1+donation each year so [join now](http://geek.zone/join)!

Issues are prioritised with the impact/urgency matrix. [P1](https://github.com/GeekZoneHQ/web/labels/P1) is the highest priority, then [P2](https://github.com/GeekZoneHQ/web/labels/P2), [P3](https://github.com/GeekZoneHQ/web/labels/P3) and finally [P4](https://github.com/GeekZoneHQ/web/labels/P4) which is the lowest priority. We are primarily focusing on the [pre-go-live](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Apre-go-live) issues at the moment. If you would like ot have a go at one/some then please feel free!

## License

As always, anything contributed to Geek.Zone projects is done so under GPLv3.
