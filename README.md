# sibl

Sandia Injury Biomechanics Laboratory (SIBL)

## Library

* XYFigure

## Getting Started

### Get a local copy of the repository using `git clone` with SSH

```bash
$ cd ~        (optional, but recommended)
$ git clone git@github.com:sandialabs/sibl.git
```

### Push to the repository

In the `~/sibl/.git/config` file, add the following:

```bash
[user]
    name = James Bond  (add you name)
    email = jb007@company.com  (your email address)
```

Configure ssh keys between your local and the repo.  This assumes to you have an existing public key file in `~/.ssh/id_rsa/id_rsa.pub`.  See [this](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) to create a public key.  See [this](https://help.github.com/en/github/authenticating-to-github) for troubleshooting.

Copy the entire **public** key to the GitHub site under [Settings > SSH and GPG keys](https://github.com/settings/keys).

From within the repo `~/sibl/`, set the username and email on a *per-repo* basis:

```bash
$ git config user.name "Alton Alternative"
$ git config user.email "alton@othercompany.com"
```

## License

* [License](LICENSE)
* [Third-Party Notice](NOTICE.md)
