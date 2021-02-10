# Geek.Zone Web App
This application is currently intended as the minimum viable product for Geek.Zone members and n00bs to be able to manage their Geek.Zone membership. We will build it from there, but that's our target right now!

We currently use a third party to manage membership, and while they are not a bad service per se, they do charge us for their services and do not do all the things we need them to do. Building it ourselves will not only mean that we get the system that we need, but also that those involved will learn new, transferrable skills and have some fun doing so. The overall target for this project is to build a system that enables a Geek.Zone member to,
* do everything they need as a member
* create real, human connections within the Geek.Zone community

We expect that, eventually, this project will also help many other membership organisations beyond Geek.Zone.

Take a look at the original [spec doc](https://docs.google.com/document/d/1c43e1wYHZhDdyiafeqodQPPd9sXDHv3pEtyxxVa64OI/edit?usp=sharing).

## Running locally
### Prerequisites
We assume that you have already done the following manual actions.  We hate manual stuff too, but these do need your input.
1. Set up [Git](https://git-scm.com/downloads)
1. (If you are on Windows) Install [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
1. Switch to the directory where you want the project files to be stored
1. Run `git clone https://github.com/GeekZoneHQ/web.git`
1. Switch into your project directory with `cd web`

If you cannot run bash, please [submit a ticket](https://github.com/GeekZoneHQ/web/issues/new).


### Install & Run
Whether it is your first time running the project, or your fifty-first time, `run.sh` is your friend. It knows whether
you have previously completed setup, so the second time it runs it just activates all the servers.

**NB:** For the sake of openness and transparency, please review `run.sh` before you run it. It needs to run lots of
`-y` (approval assumed) flags in `sudo`, so you will probably want to know what you are agreeing to before you charge in.

When you are ready,

1. Run `sudo sh run.sh`
1. Get [coffee](http://geek.zone/amazon) (not required but super helpful)
1. Done

## Local Development

### Running the Tests

Simply run `python manage.py test` before you PR.

### Changing the CircleCI Build

We have found the [circleci local cli tool](https://circleci.com/docs/2.0/local-cli/) to be very useful when making changes to the circle build locally. The errors can be a bit cryptic, but it's easier than debugging basic syntax issues from within the circleci console.

## Contributing

Before you ask, we use [spaces](https://www.youtube.com/watch?v=SsoOG6ZeyUI).

1. Do the *Prerequisites* steps in *Running the project locally* above
1. [Join GitHub](https://github.com/join)
1. [Join Geek.Zone](https://geek.zone/join)
1. Set up [SSH access to GitHub](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)
1. Set up [GitHub 2FA](https://docs.github.com/en/github/authenticating-to-github/configuring-two-factor-authentication)
1. (If you do not already have one) Generate a [GPG key](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-gpg-key)
1. Add your [GPG key to GitHub](https://docs.github.com/en/github/authenticating-to-github/adding-a-new-gpg-key-to-your-github-account)
1. [Talk to James](https://calendly.com/geekzone-james/30min) about joining the project

While we are grateful for any and all contributions, we are mainly focusing on providing Geek.Zone members with the tools required to contribute at this time. Membership is just £1 + donation, so we hope that this is a very low barrier to entry. We will work on improving this in the future.

Otherwise, we have no special rules, just follow the [open source guide](https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution). Little and often commits are often a good idea. If you wish to add your name and contact details to humans.txt then you are encouraged to do so. Not obligatory.

Issues are prioritised with the impact/urgency matrix. [P1](https://github.com/GeekZoneHQ/web/labels/P1) is the highest priority, then [P2](https://github.com/GeekZoneHQ/web/labels/P2), [P3](https://github.com/GeekZoneHQ/web/labels/P3) and finally [P4](https://github.com/GeekZoneHQ/web/labels/P4) which is the lowest priority. We are primarily focusing on the [pre-go-live](https://github.com/GeekZoneHQ/web/issues?q=is%3Aissue+is%3Aopen+label%3Apre-go-live) issues at the moment. If you would like ot have a go at one/some then please feel free!

## Suggestions

Clearly, you can and should use which ever development tools you prefer. If you don't have a preference, we suggest trying,

#### Python
 * [PyCharm](https://www.jetbrains.com/pycharm/)
 * [Visual Studio Code](https://code.visualstudio.com/)
#### SQL
 * [DBeaver Community Edition](https://dbeaver.io/)
#### Diagrams
 * [DrawIO Desktop](https://github.com/jgraph/drawio-desktop/releases/) (required for ERD)

Also, do join us on our [Discord](https://geek.zone/discord)!


## License

As always, anything contributed to Geek.Zone projects is done so under GPLv3.
