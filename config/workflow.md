# Developer Workflow

```bash
> cd ~/sibl
> conda activate siblenv
> git pull
```

## Use Gitflow with Git

Git-flow is a wrapper around Git.  The `git flow init` command is an extension of the
default git init command and doesn't change anything in the repository other than 
creating branches for you.

* [Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
* [Example](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/init-Gitflow-example-workflow-tutorial)

```bash
> git flow init  # and accept all defaults as shown below
⋊> ~/sibl on master ◦ git flow init                  (siblenv)  Fri Jul 23 16:33:18 2021

Which branch should be used for bringing forth production releases?
   - master
Branch name for production releases: [master]
Branch name for "next release" development: [develop]

How to name your supporting branch prefixes?
Feature branches? [feature/]
Release branches? [release/]
Hotfix branches? [hotfix/]
Support branches? [support/]
Version tag prefix? []
⋊> ~/sibl on develop
```

Augment the default `master` branch (`main` is now often used instead of `master`) with 
a `develop` branch.  A simple way to do this is for one developer to create an empty 
`develop` branch locally and push it to the server:

```bash
⋊> ~/sibl on develop
⨯> git push -u origin develop                        (siblenv)  Fri Jul 23 16:34:32 2021
Total 0 (delta 0), reused 0 (delta 0)
remote:
remote: Create a pull request for 'develop' on GitHub by visiting:
remote:      https://github.com/sandialabs/sibl/pull/new/develop
remote:
To github.com:sandialabs/sibl.git
 * [new branch]      develop -> develop
Branch 'develop' set up to track remote branch 'develop' from 'origin'.
⋊> ~/sibl on develop ⨯
```

Other developers should now clone the central repository and create a tracking 
branch for the `develop` branch:

```bash
$ git flow init

Initialized empty Git repository in ~/project/.git/
No branches exist yet. Base branches must be created now.
Branch name for production releases: [master]
Branch name for "next release" development: [develop]

How to name your supporting branch prefixes?
Feature branches? [feature/]
Release branches? [release/]
Hotfix branches? [hotfix/]
Support branches? [support/]
Version tag prefix? []

$ git branch
* develop
  master
```

Now create a feature branch:

```bash
> git flow feature start feature_branch
```

To push the current branch and set the remote as upstream, use

```bash
> git push --set-upstream origin feature/feature_branch
```

The proceed with local implementation, and `git commit -m 'message'` and `git push` to push
local implementation up to the repo on the `feature_branch`.

When the feature implementation is completed, to merge the `feature_branch` into the `develop` branch:

```bash
> git flow feature finish feature_branch
```

## Pytest and Coverage

```bash
# ----
# sync
# ----
$ (base) [~]$ cd ~/sibl
$ (base) [~/sibl] git status
$ (base) [~/sibl] git pull
$ (base) [~/sibl] git add, git commit -m "message", git push
#
# ---------
# implement
# ---------
$ (base) [~/sibl]$ conda activate siblenv
$ (siblenv) [~/sibl]$ # development
#
# ------
# pytest
# ------
# check unit tests
$ (siblenv) [~/sibl]$ pytest # unit tests must pass prior to push to repository
$ (siblenv) [~/sibl]$ pytest -v # for more verbose unittest output
#
# ---------
# blacktest
# ---------
$ (siblenv) [~/sibl] black --check .
#
# or to check specific folders one at a time
$ (siblenv) [~/sibl] black --check cli/
$ (siblenv) [~/sibl] black --check geo/
#
# if above check failse, the diff or fix 
# diff: (without automatic code modification)
$ (siblenv) [~/sibl] black --check some_specific_file.py --diff 
$ (siblenv) [~/sibl] black --check some_folder/ --diff
# fix: (with automatic code modification)
$ (siblenv) [~/sibl] black some_specific_file.py
$ (siblenv) [~/sibl] black some_folder/
$ (siblenv) [~/sibl]
#
# ---------
# covertest
# ---------
$ (siblenv) [~/sibl]$ pytest --cov=.
#
# or to test specific folders
$ (siblenv) [~/sibl]$ pytest --cov=cli/src/xyfigure --cov=geo/src/ptg
#
# and to add missing coverage line number reporting
$ (siblenv) [~/sibl]$ pytest --cov=cli/src/xyfigure --cov=geo/src/ptg  --cov-report term-missing
```
