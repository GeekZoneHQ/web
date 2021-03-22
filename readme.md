# Geek.Zone Web App
This application is currently intended as the minimum viable product for Geek.Zone members and n00bs to be able to
manage their Geek.Zone membership. We will build it from there, but that's our target right now! We currently use a
third party to do this, and while they are not a bad service per se, they do charge us for their services and do not do
all the things we need them to do. Building it ourselves will not only mean that we get the system that we need, but
also that those involved will learn new, transferrable skills and have some fun doing so.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

# Progress so far
Here's what the front page looks like in [light mode](/screencapture-gzweb-light-2021-03-22-20_23_50.png) and in
[dark mode](/screencapture-gzweb-dark-2021-03-22-20_24_03.png).

## Running the project locally

You should be able to setup this project on any operating system that supports Django. We have instructions for Ubuntu based linux distributions which can be found below; Windows instructions are in the pipeline.

### Ubuntu based Linux (or WSL on Microsoft Windows)

> This guide assumes that you can execute basic terminal commands. It also assumes that you have setup github with SSH keys.

Ubuntu 20.04 and above should come with a recent enough version of Python 3 for you to follow along with this guide. As of writing I am using Python 3.8.5.

First follow the instructions below for initial setup.

1. Install the Python package manager `pip` by running the command `sudo apt install python3-pip`
2. Install virtualenv using the command `python3 -m pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
3. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
4. Create a virtual environment `python3 -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
5. Activate the virtual environment `source env/bin/activate`.
6. Install the project dependencies `pip install -r requirements.txt`
7. Create the local database by running the migrations `python manage.py migrate`
1. Install RabbitMQ `sudo apt-get install rabbitmq-server`
1. Run RabbitMQ `sudo systemctl enable rabbitmq-server`
1. Run the celery worker `celery -A web worker --loglevel=info`
8. Run the local server `python manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

The above instructions should be enough to get the Django server running, and the membership management software accessible from a browser. There is a small amount of additional configuration required for a fully working system, which is OS agnostic. We will be producing a guide for this additional configuration soon.

After you have done the above subsequent setup is a lot simpler.
```sh
source env/bin/activate # You only need to do this if your virtual env is not already active
python manage.py runserver
```

If there are new changes to the database the runserver output will run you through the process of updating and running the migrations.

#### Running RabbitMQ & Celery independently
RabbitMQ & Celery have been purposefully implemented in a way that allows them to be used in any part of the project.
Equally, this also allows them to be used interactively in the Django Python shell.
1. Install RabbitMQ `sudo apt-get install rabbitmq-server`
1. Run RabbitMQ `sudo systemctl enable rabbitmq-server`
1. Run the celery worker `celery -A web worker --loglevel=info`
1. `python3 manage.py shell`
1. `from memberships import tasks, email`
1. `import celery`
1. Run a task function from `tasks.py`, such as
   `tasks.task_send_email("Bob", "weoifjefij@mailinator.com", "Hello world", "Just a test")`
   
You will need the password if you want to send from an @geek.zone email address. Please contact
@JamesGeddes for this or configure your own testing email address in `settings.py`.


### Microsoft Windows (Without WSL)

> The following steps have only been tried on Windows 10 Pro in a virtual machine

1. Install Git for windows by downloading a copy from https://git-scm.com/download/win
2. Install Python from the Microsoft store. Typing `python` into a command prompt will open the correct page on the Microsoft store. This will also install the `pip` package manager.
3. Install virtualenv using the command `pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
4. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
4. Create a virtual environment `python3 -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
5. Activate the virtual environment `env\Scripts\activate.bat`
6. Install the project dependencies `pip install -r requirements.txt`
7. Create the local database by running the migrations `python manage.py migrate`
8. Run the local server `python manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

The above instructions should be enough to get the Django server running, and the membership management software accessible from a browser. There is a small amount of additional configuration required for a fully working system, which is OS agnostic. We will be producing a guide for this additional configuration soon.

## Local Development

### Working on the front-end code

> All commands in this section need to be run in the virtual environment.

The website currently uses Tailwind CSS to style the front end. Tailwind works by generating a stylesheet at `theme/static/css/styles.css`, using settings located in `theme/static_src` (with base styles at `theme/static_src/src/styles.scss`).

A development build of `styles.css` already exists in the repository, containing all possible Tailwind base styles. Therefore, only install and run Tailwind if you plan on making changes to settings or base styles at `theme/static_src` (or you want to generate a production build of `styles.css`). You do not need to install and run Tailwind to make simple styling changes.

#### Installing Tailwind

You will need to ensure Node.js and NPM are installed on your system first - Node.js must be version 12.13.0 or higher.

Once that's done, run:
```sh
python manage.py tailwind install
```

>You will need to run this command again if you ever upgrade Node.js.

#### Running Tailwind alongside the local server

When running the local server, run the following in a second terminal/command prompt:
```sh
python manage.py tailwind start
```

This will re-generate the development build of `styles.css`, then watch for any changes made to files in `theme/static_src`.

>A production build of `styles.css` can be generated using the command `python manage.py tailwind build` - this reduces the file to only the base styles that are actually being used.

If you want to use LiveReload to automotically refresh your web browser in response to file changes, run the following in another terminal/command prompt
```sh
python manage.py livereload
```

### Suggested tools

Clearly, you can and should use which ever development tools you prefer. If you don't have a preference, we suggest trying,

#### General coding
 * [Visual Studio Code](https://code.visualstudio.com/)
#### Python
 * [PyCharm](https://www.jetbrains.com/pycharm/)
#### SQL
 * [DBeaver Community Edition](https://dbeaver.io/)
#### Diagrams
 * [DrawIO Desktop](https://github.com/jgraph/drawio-desktop/releases/tag/v13.3.1)

Also, do join us on our [Discord](https://geek.zone/discord)!

### Running the Tests

Simply run `python manage.py test`.

### Changing the CircleCI Build

We have found the [circleci local cli tool](https://circleci.com/docs/2.0/local-cli/) to be very useful when making changes to the circle build locally. The errors can be a bit cryptic, but it's easier than debugging basic syntax issues from within the circleci console.

## Contributing

Before you ask, we use [spaces](https://www.youtube.com/watch?v=SsoOG6ZeyUI).

Otherwise, no special rules, just pull request before merging, you know the drill ;) Little and often commits are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Geek.Zone members are invited to the Geek.Zone org on GitHub so that they can contribute directly. Membership only costs £1+donation each year so [join now](http://geek.zone/join)!

Issues are prioritised with the impact/urgency matrix. [P1](https://github.com/GeekZoneHQ/web/labels/P1) is the highest priority, then [P2](https://github.com/GeekZoneHQ/web/labels/P2), [P3](https://github.com/GeekZoneHQ/web/labels/P3) and finally [P4](https://github.com/GeekZoneHQ/web/labels/P4) which is the lowest priority. We are primarily focusing on the [pre-go-live](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Apre-go-live) issues at the moment. If you would like to have a go at one/some then please feel free!

## License

As always, anything contributed to Geek.Zone projects is done so under GPLv3.
