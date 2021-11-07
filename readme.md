# Geek.Zone Web App
This application is currently intended as the minimum viable product for Geek.Zone members and n00bs to be able to manage their Geek.Zone membership. We will build it from there, but that's our target right now! We currently use a third party to do this, and while they are not a bad service per se, they do charge us for their services and do not do all the things we need them to do. Building it ourselves will not only mean that we get the system that we need, but also that those involved will learn new, transferrable skills and have some fun doing so.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

# Progress so far
Here's what the front page looks like in [light mode](/screencapture-gzweb-light-2021-03-22-20_23_50.png) and in
[dark mode](/screencapture-gzweb-dark-2021-03-22-20_24_03.png).

## Running the project locally

You should be able to setup this project on any operating system that supports Django. We have instructions for Ubuntu based linux distributions and for Windows 10. Both can be found below.
Alternatively you can run this project in containers, by using docker-compose.

### Ubuntu based Linux (or WSL on Microsoft Windows)

> This guide assumes that you can execute basic terminal commands. It also assumes that you have setup github with SSH keys.

Ubuntu 20.04 and above should come with a recent enough version of Python 3 for you to follow along with this guide. As of writing I am using Python 3.8.5.

First follow the instructions below for initial setup.

1. Install the Python package manager `pip` by running the command `sudo apt install python3-pip`
2. Install virtualenv using the command `python3 -m pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
3. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
4. Create a virtual environment `python3 -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
5. Activate the virtual environment `source env/bin/activate`
6. Install libpq-dev package required by psycopg2 `sudo apt-get install libpq-dev`
7. Install the project dependencies `pip install -r requirements.txt`
8. Install Postgres database `sudo apt-get -y install postgresql` 
9. Configure Postgres to start on boot `sudo systemctl enable postgresql`
10. Switch user environment to postgres user `sudo su postgres`
11. Run the Postgres interactive terminal `psql`
12. Change/assign password to postgres user `\password postgres` 
13. Type a new password, (e.g. 'postgres'). This password has to match whatever is configured in step 16
14. Exit from postgres database terminal `exit` 
15. Exit from postgres user environment `exit`
16. Create an .env file with parameters for local development. Add any extra parameters as needed:
```sh
cat <<EOF > web/.env
DEBUG=1
DATABASE_USER=postgres
DATABASE_NAME=postgres
DATABASE_HOST=localhost
DATABASE_PASSWORD=postgres
DATABASE_PORT=5432
EOF
```
17. Run the database migrations `python3 manage.py migrate`
18. Install RabbitMQ `sudo apt-get install rabbitmq-server`
19. Configure RabbitMQ to start on boot `sudo systemctl enable rabbitmq-server`
20. Run the celery worker `celery -A web worker --loglevel=info`
21. Open another terminal and run the local server `python3 manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

After you have done the above subsequent setup is a lot simpler.
```sh
source env/bin/activate # You only need to do this if your virtual env is not already active
python manage.py runserver
```

If there are new changes to the database the runserver output will run you through the process of updating and running the migrations.


### Microsoft Windows (Without WSL)

> This guide assumes that you can execute basic terminal/Powershell commands. It also assumes that you have setup github with SSH keys.
Currently the project needs some adjustments to run in Windows. Specifically the USER and PASSWORD variables for Postgres need either to be hard-coded in settings.py or passed through cli when running database migrations.

1. Install Git for windows by downloading a copy from https://git-scm.com/download/win
2. Install Python from the Microsoft store. Typing `python` into a command prompt will open the correct page on the Microsoft store. This will also install the `pip` package manager.
3. Install virtualenv using the command `pip install virtualenv`. This tool allows us to install dependencies local to a project and not clutter your system.
4. Clone this repository to your desired location `git clone git@github.com:geekzonehq/web.git` and change into that directory `cd web`.
5. Create a virtual environment `python -m virtualenv env`. This will create a folder in the project called `env` that will contain all of the project dependencies.
6. Activate the virtual environment `env\Scripts\activate.bat`
7. Install Postgresql from this link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
8. Run the installation wizard, choose a password for the database superuser (postgres) and accept all subsequent defaults, click on "Finish" 
9. Press Win+R and type `services.msc`: scroll down to the postgres-service=name and start it if it is not already running. If the option to start the service is greyed out, configure Postgres to start on boot: right-click on the postgres-service-name, click on `Properties` and set the `Startup type` to `Automatic`.
The same can be achieved by running as administrator a couple of Powershell commands:
```PS
Install-Module PostgreSQLCmdlets
Set-Service -Name "<<postgres-service-name>>" -Status running -StartupType automatic
```
10. Create an .env file with parameters for local development. Add any extra parameters as needed:
```PS
echo "DEBUG=1
DATABASE_USER=postgres
DATABASE_NAME=postgres
DATABASE_HOST=localhost
DATABASE_PASSWORD=postgres
DATABASE_PORT=5432" | tee web/.env
``` 
11. Install the project dependencies `pip install -r requirements.txt`
12. Run the database migrations `python manage.py migrate`
13. Install Erlang for Windows using an administrative account from this link: https://erlang.org/download/otp_versions_tree.html
14. Download and run the latest Rabbitmq installer from this page: https://github.com/rabbitmq/rabbitmq-server/releases. Rabbitmq service should already be running, otherwise start it from the start menu
12. Run the celery worker `celery -A web worker --loglevel=info`
13. Open another terminal and run the local server `python manage.py runserver`. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit the server.

After you have done the above subsequent setup is a lot simpler.
```PS
env\Scripts\activate.bat # You only need to do this if your virtual env is not already active
python manage.py runserver
```

If there are new changes to the database the runserver output will run you through the process of updating and running the migrations.


#### Running RabbitMQ & Celery independently (same configuration for Ubuntu and Windows 10)
RabbitMQ & Celery have been purposefully implemented in a way that allows them to be used in any part of the project.
Equally, this also allows them to be used interactively in the Django Python shell.
1. Make sure RabbitMQ is running (Ubuntu: `sudo systemctl start rabbitmq-server`; Windows 10: run Powershell as administrator `Start-Service RabbitMQ`)
1. Run the celery worker `celery -A web worker --loglevel=info`
1. `python manage.py shell`
1. `from memberships import tasks, email`
1. `import celery`
1. Run a task function from `tasks.py`, such as
   `tasks.task_send_email("Bob", "weoifjefij@mailinator.com", "Hello world", "Just a test")`
   
You will need the password if you want to send from an @geek.zone email address. Please contact
@JamesGeddes for this or configure your own testing email address in `settings.py`.


### Install docker & docker-compose

#### Linux/Ubuntu
```sh
# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io

# Configure docker to start on boot
sudo systemctl enable docker.service

# Manage Docker as a non-root user
sudo groupadd docker
sudo usermod -aG docker $USER
```
Log out of your session completely and then log back in

```sh
# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
```sh
# Install command completion
sudo curl \
    -L https://raw.githubusercontent.com/docker/compose/1.29.2/contrib/completion/bash/docker-compose \
    -o /etc/bash_completion.d/docker-compose
source ~/.bashrc
```
#### Windows 10

Follow the instructions in the Docker documentation https://docs.docker.com/desktop/windows/install/; the installation varies depending on the Windows 10 edition. Docker Desktop for Windows includes Compose, so there is no need to install it separately. Once the installion is complete, right-click on the Docker icon in the system tray, and `Switch to Linux Containers` if Docker Desktop is set to Windows Containers.

### Running the project in docker containers

An `.env.dev` file under the `web` folder is already existing and provides environment variables to docker-compose.
1. Make sure Docker is running (Ubuntu: `sudo systemctl restart docker`; Windows 10: run Powershell as administrator `Start-Service 'Docker Desktop Service'`)
2. `docker-compose up` (to run containers when the images are already present in the machine; if not existing they will be created)
3. `docker-compose --build` (to build images for each service outlined in the docker-compose.yml file)
4. `docker-compose up --build` (to force to build images and run containers out of these images; this is useful when making changes to the project folder to test real time those changes)
5. `docker-compose ps` (from another terminal window, to check of status of each container created by docker-compose)
6. If you navigate to `http://localhost:8000/memberships/register` in your browser you should now see the app. You can press control-c in the terminal to exit docker-compose.
7. `docker-compose down` (to delete the network and containers that docker-compose created)

## Local Development

### Working on the front-end code

> All commands in this section need to be run in the virtual environment.

The website currently uses Tailwind CSS to style the front end. Tailwind works by generating a stylesheet at `theme/static/css/dist/styles.css`, using settings located in `theme/static_src` (with base styles at `theme/static_src/src/styles.scss`).

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

If you want to use LiveReload to automatically refresh your web browser in response to file changes, run the following in another terminal/command prompt:
```sh
python manage.py livereload
```

#### Suggested tools

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

We try to be super informal, and we welcome all PRs. For full details, see [CONTRIBUTING](CONTRIBUTING.md).

## License

Geek.Zone is a member of the [Open Source Initiative](https://opensource.org/osi-affiliate-membership), so all our
projects are published under GPLv3. Any contributions you make will be published under these provisions. See
[LICENSE](LICENSE).
