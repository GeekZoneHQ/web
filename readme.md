# Geek.Zone Web App
## TL;DR
**What?**

Open source Python Django project

**Why?**
* To allow all Geek.Zone members to do everything they need as part of their membership
*  Should be helpful to other community organisations too

**How?**
*  MVP is membership management.
*   Have a [chat with James](http://calendly.com/geekzone-james/30min) and get involved!  

## Current State
> [You're going to need a bigger boat](https://www.youtube.com/watch?v=2I91DJZKRxs)

We currently use a third party, [membermojo](https://membermojo.co.uk/), to allow Geek.Zone members to manage their own membership. It does work, but falls short in several ways;
* Forces the *firstname, lastname* structure; [bad, bad, bad](https://www.w3.org/International/questions/qa-personal-names#singlefield)
* No API access; "we currently have no plans for this" (membermojo Customer Support)
* Cannot handle membership upgrades; needed for [Space Membership](http://geek.zone/space)
* on top of all the above, they charge us

The www.Geek.Zone website is run on TikiWiki which, while powerful, also has some limitations;
* built in PHP; [everyone hates PHP](https://www.google.com/search?q=php+memes)
* [not widely used](https://www.glassdoor.co.uk/Job/tikiwiki-jobs-SRCH_KE0,8.htm); skills gained are not transferable
* not really set up for paid membership

## Market Research
> [These aren't the droids you're looking for](https://www.youtube.com/watch?v=ihyjXd2C-E8)

We have used other platforms, such as,

### Oxwall

**Negatives**
* built in PHP; again, everyones "favourite" language
* Many [fundamental flaws](https://developers.oxwall.com/forum/topic/51458)
* Geek.Zone members found it clunky

### MediaWiki
**Positives**
* Powers ruddy Wikipedia
* Widely used

**Negatives**
* Yet more blasted PHP
* Not great for social functionality

## Goal
> [This is my boomstick!](https://www.youtube.com/watch?v=zdkqagOUaPM)

The end-game goal of this project is twofold. The primary goal is to create a platform that all Geek.Zone members can use for everything they need as a Geek.Zone member. This will include,
* join Geek.Zone
* manage their membership
* set up donations
* join groups within Geek.Zone
* post in forums
* edit www.Geek.Zone in the wiki way
* publish blogs

...as well as much more. In short, this will take over from TikiWik to *be* the website and allow us to automate as much as possible to better respect volunteer time. Take a look at our [future-work](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Afuture-work) tickets to get an idea of some of the ideas we have had so far.

The secondary (longer term) goal is to make the platform useful to other groups so that,
* they can better manage their own members
* Geek.Zone can create a [funding source](https://github.com/GeekZoneHQ/web/issues/142) by hosting the platform for those groups who don't have the capacity to do it themselves.
* we can offer additional training opportunities to our members

## Priority
> [A cunning plan, my lord](https://youtu.be/ACnqI1l4I9s?t=21)

Our main immediate aim is to provide a minimum viable product for Geek.Zone members and n00bies to be able to manage their Geek.Zone membership, allowing us to retire membermojo. We will build it from there, but that's our target right now! Building it ourselves will not only mean that we get the system that we need, but also that those involved will learn new, transferrable skills and have some fun doing so.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

## Running the project locally

You should be able to setup this project on any operating system that supports Django. Please submit a ticket if you have any difficulties.

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

1. Install [git for windows](https://git-scm.com/download/win)
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

No special rules, just pull request before merging, you know [the drill](https://opensource.guide/how-to-contribute/) :smile: Little and often commits & comments are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Geek.Zone members are invited to the Geek.Zone org on GitHub so that they can contribute directly. Membership only costs £1+donation each year so [join now](http://geek.zone/join)! Have a [chat with James](http://calendly.com/geekzone-james/30min) and get involved! 


Issues are prioritised with the impact/urgency matrix. [P1](https://github.com/GeekZoneHQ/web/labels/P1) is the highest priority, then [P2](https://github.com/GeekZoneHQ/web/labels/P2), [P3](https://github.com/GeekZoneHQ/web/labels/P3) and finally [P4](https://github.com/GeekZoneHQ/web/labels/P4) which is the lowest priority. We are primarily focusing on the [pre-go-live](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Apre-go-live) issues at the moment. If you would like to have a go at one/some then please feel free!

## License

As always, anything contributed to this and any other Geek.Zone project is done so under GPLv3.
