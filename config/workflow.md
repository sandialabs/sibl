# Developer Workflow

```bash
# after the repository has been cloned and then siblenv environment is set up
> cd ~/sibl
> conda activate siblenv
> git pull  # update your local from the repository

# code
# ... do your development work ...

# contribute your development to the repository:
# prior to committing to the repository, test for quality and style and resolve any errors
> cd ~/sibl
> ./quality
> ./style

# commit to the repositiory
> git commit -m 'some descriptive message of your contribution'
> git push
```

## Frequently Asked Questions

### Q: How do I rebase my branch with develop?

```bash
> git checkout develop  # check out the develop branch on your local

# Fetch the remote version of the develop branch and merge it
# (or rebase it, depending on your pull strategy) into/onto your local branch.
# This assures that the remote version and the local version of develop are the same
> git pull origin develop

> git checkout feature-branch  # check out the local feature branch

> git rebase develop
```

### Q: How do I fix the `HEAD detached at <commit_hash>` state?

A: See https://www.cloudbees.com/blog/git-detached-head, Git Detached Head: What This Means and How to Recover, G Patru, 2020-07-15.

### Notes

* 2022-01-06:
  * [Use of Gitflow was deprecated](deprecated.md#deprecated-use-of-gitflow).
  * [Manual test and coverage was deprecated](deprecated.md#manual-test-and-coverage).

