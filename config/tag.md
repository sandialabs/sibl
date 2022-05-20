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

Sharing Tags:  By default, the git push command does not transfer tags to remote servers. You will have to explicitly push tags to a shared server after you have created them. This process is just like sharing remote branches — you can run `git push origin <tagname>`.

```bash
$ git push origin v0.0.1
Enumerating objects: 1, done.
Counting objects: 100% (1/1), done.
Writing objects: 100% (1/1), 157 bytes | 157.00 KiB/s, done.
Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
To github.com:sandialabs/sibl.git
 * [new tag]         v0.0.1 -> v0.0.1
```

## References

* [GitHub book](https://git-scm.com/book/en/v2/Git-Basics-Tagging)