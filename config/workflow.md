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

### Notes

* 2022-01-06:
  * [Use of Gitflow was deprecated](deprecated.md#deprecated-use-of-gitflow).
  * [Manual test and coverage was deprecated](deprecated.md#manual-test-and-coverage).
