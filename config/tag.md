# Git Tag

## Read

View current tags:

```bash
$ git tag
$ git tag -l
$ git tag --list
```

View tags with a filter:

```bash
$ git tag -l "v1.8.5*"  # for example
```

## Create

* Two types of tags, lightweight and annotated, prefer annotated.
* Use the `-a` option to createa an annotated tag.

```bash
$ git tag -a v0.0.1 -m "first tag"
$ git tag
v0.0.1
```

## References

* [GitHub book](https://git-scm.com/book/en/v2/Git-Basics-Tagging)