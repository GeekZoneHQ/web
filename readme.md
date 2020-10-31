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

We have not got any tests for you right now. This readme will be kept up to date so check back when it does.

### Changing the CircleCI Build

We have found the [circleci local cli tool](https://circleci.com/docs/2.0/local-cli/) to be very useful when making changes to the circle build locally. The errors can be a bit cryptic, but it's easier than debugging basic syntax issues from within the circleci console.

### Running Kubernetes files locally

The kubernetes files are not optimised for being run locally (yet), but you should be able to get them working with minimal local changes.

We use envsubst in the build to replace the image tag numbers in the kubernetes yaml files. You can run the same command locally if you wish.

```sh
CIRCLE_WORKFLOW_ID=1 envsubst < k8s/deployment.yml | kubectl apply -f -
```

## Deployment

The code is currently deployed onto a test Kubernetes cluster hosted using AWS Elastic Kubernetes Service (EKS). Our CI/CD service [circleci](https://circleci.com/) will deploy any code changes to [test.geek.zone](http://test.geek.zone/) on a merge to master.

The deployment files can be found under the `k8s` folder.

## Contributing

No special rules, just pull request before merging, you know the drill ;) Little and often commits are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Geek.Zone members are invited to the Geek.Zone org on GitHub so that they can contribute directly. Membership only costs £1+donation each year so [join now](http://geek.zone/join)!

## License

As always, anything contributed to Geek.Zone projects is done so under GPLv3.
