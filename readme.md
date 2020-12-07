# Geek.Zone Web App
This application is currently intended as the minimum viable product for Geek.Zone members and n00bs to be able to manage their Geek.Zone membership. We will build it from there, but that's our target right now! We currently use a third party to do this, and while they are not a bad service per se, they do charge us for their services and do not do all the things we need them to do. Building it ourselves will not only mean that we get the system that we need, but also that those involved will learn new, transferrable skills and have some fun doing so.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
What things you need to install the software and how to install them

* Python==3.8.3 (Not compatible with Windows XP (why are you still using Windows XP?))
* Pip==3
* Django==3.0.7
* PostgreSQL==12.3

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

### Installing

Here's what to do to get this project up and running so that you can turn that sweet, sweet coffee in to sweet, sweet code.

1. Linux: `sudo apt-get update && sudo apt-get upgrade`. Windows: install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).
1. Get the latest version of [Python3](https://www.python.org/downloads/)
1. Pip3 should come with python. Double check.
1. In a convenient, empty directory, run `git clone git@github.com:GeekZoneHQ/web.git`
1. [Create a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) in that directory
1. Activate that virtual environment
1. Run `pip3 install -r requirements.txt`
1. Check if you have already got [PostgreSQL](https://www.postgresql.org/download/). Install it if not.


## Local Development

### Running the Tests

Simply run `python manage.py test`.

### Changing the CircleCI Build

We have found the [circleci local cli tool](https://circleci.com/docs/2.0/local-cli/) to be very useful when making changes to the circle build locally. The errors can be a bit cryptic, but it's easier than debugging basic syntax issues from within the circleci console.

## Contributing

No special rules, just pull request before merging, you know the drill ;) Little and often commits are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Geek.Zone members are invited to the Geek.Zone org on GitHub so that they can contribute directly. Membership only costs £1+donation each year so [join now](http://geek.zone/join)!

Issues are prioritised with the impact/urgency matrix. [P1](https://github.com/GeekZoneHQ/web/labels/P1) is the highest priority, then [P2](https://github.com/GeekZoneHQ/web/labels/P2), [P3](https://github.com/GeekZoneHQ/web/labels/P3) and finally [P4](https://github.com/GeekZoneHQ/web/labels/P4) which is the lowest priority. We are primarily focusing on the [pre-go-live](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Apre-go-live) issues at the moment. If you would like ot have a go at one/some then please feel free!

## License

As always, anything contributed to Geek.Zone projects is done so under GPLv3.
