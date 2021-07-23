# Developer Workflow

```bash
> cd ~/sibl
> conda activate siblenv
> git pull
```

Use Gitflow with Git

Git-flow is a wrapper around Git.  The `git flow init` command is an extension of the
default git init command and doesn't change anything in the repository other than 
creating branches for you.

* [Tutorial](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
* [Example](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/init-Gitflow-example-workflow-tutorial)

```bash
> git flow init
```


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
