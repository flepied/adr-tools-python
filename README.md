# README #

This is a project to get a python equivalent of the adr-tools by npryce on [github][adr-tools]. The tool can make and list and change Architecture Decision Records. For more information on Architecture Decision Records see the page of [Joel Parker Henderson on ADRs](https://github.com/joelparkerhenderson/architecture_decision_record).

Forked from https://bitbucket.org/tinkerer_/adr-tools-python/ to suit my needs:

- use [MADR](https://adr.github.io/madr/) format
- generate an `index.md` file each time a new ADR is created
- template stored in the project under `.template.md`
- filenames in lowercase
- optional template directory used to bootstrap the first ADR and the stored template
- use an `init.md` template if it exists for the first ADR created by `adr-init`
- reformat Python code with black
- add some tests

## Installation

```
pip install git+https://github.com/flepied/madr-tools-python@template
```

or

```
python3 -m pip install git+https://github.com/flepied/madr-tools-python@template --user
```
By adding a `--upgrade` flag, the tool can be updated if a new version is available

## Usage

### adr-init

With `adr-init`, the directory structure can be initialized. Default, a subdirectory `doc/adr` is generated and populated with a default template in `.template.md`, but if a different directory is wished for, this can be input:

```
adr-init foo
```

In this case, adrs will be stored in a local folder `foo/`. In the main directory, a file called `.adr-dir` is generated to indicate to `adr-tools` that a different location than the default `doc/adr/` is used. This behaviour was copied from, and should be compatible with the original [adr-tools][]. `adr-init` always creates a new adr to say that adrs will be used. 

If you have your own templates, you can specify the directory where to find the templates with`-t` to `adr-init`. If there is an `init.md` file, it is used as the first ADR else the default template is used.

In the template file, you can specify the following strings that will be automatically replaced:

- `NUMBER`: index of the ADR
- `TITLE`: title of the ADR passed on the command line with a capitalized first word
- `DATE`: date of the day

The tools expect to have the first line like this in the templates:

```
# NUMBER. TITLE
```

and the Status line to be like that:

```
<prefix>Status: <status>
```

if you want to move away from this, you will have to modify the code.

### adr-new

A subject should be given for a new adr:

```
> adr-new Create equal animals
> adr-list
doc/adr/0001-record-architecture-decisions.md
doc/adr/0002-create-equal-animals.md
> 
```
ADRs can be superceded from the command line using the `-s` option, and be linked by using the `-l` option. 

From the documentation of [adr-tools][https://github.com/npryce/adr-tools#quick-start]:

```
> # Multiple -s and -l options can be given, so that the new ADR can supercede
> # or link to multiple existing ADRs.
> ##
> # E.g. to create a new ADR with the title "Use MySQL Database":
> ##
> adr new Use MySQL Database
> ##
> # E.g. to create a new ADR that supercedes ADR 12:
> ##
> adr new -s 2 Use PostgreSQL Database
> ##
> # E.g. to create a new ADR that supercedes ADRs 3 and 4, and amends ADR 5:
> ##
> adr new -s 2 -s 3 -l "4:amends:amended by" Use Riak CRDTs to cope with scale
> ##
```

The same funcitonality is also available in this python version

### adr-list

See above, lists the adrs.

### Serving the adrs

If you want the ADRs to be served on a webpage, please look for the python package [adr-viewer](https://pypi.org/project/adr-viewer/

## Source, contribution

The source code is available on [Github](https://github.com/flepied/madr-tools-python). If you're interested in collaborating let me know, and/or send a pull request.

## Thanks

Thanks to Michael Nygard for the original [idea of ADRs](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions), WesleyKS for his work on [adre](https://github.com/wesleyks/adre/tree/master/adre) (which was inspiring, but not the road I followed), and of course to Npryce for making and documenting the [bash toolchain][adr-tools] I tried to replicate in Python.

[adr-tools]: https://github.com/npryce/adr-tools
