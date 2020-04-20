import os
from os import listdir
from os.path import isfile, join
import fileinput
import re

# To copy files
from shutil import copyfile
from datetime import date

_VALID_FILENAME_REGEXP = re.compile(r"\d{4,4}.*\.md")

# by default, do not print.
# Most hints on using variables came from this page: https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
# variable is a list, because lists are mutable.
__adr_verbose = [False]


def get_adr_verbosity():
    return __adr_verbose[0]


def set_adr_verbosity(verbosity):
    adr_print("verbosity set to " + str(verbosity))
    if verbosity:
        print("Verbose printing is enabled")
        __adr_verbose[0] = True
    else:
        # print('silent...')
        __adr_verbose[0] = False


# adr-config:
# Original bash implementation generates strings with paths to
# bin and template dir (both the same).

# In this python implementation I've changed this to a
# dictionary. I think this is more future proof and way
# more 'pythonic' and less error prone.


def adr_print(text):
    if get_adr_verbosity():
        print(text)


def adr_config(template_dir=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = {
        "adr_bin_dir": dir_path,
        "adr_template_dir": template_dir if template_dir else dir_path,
    }
    return config


# adr-init

# file IO:
# https://docs.python.org/3/tutorial/inputoutput.html


def adr_init(config, localpath, dirname):
    if str(dirname) != "doc/adr/":
        with open(".adr-dir", "w") as f:
            f.write(dirname)
    # create subdirectories
    # https://stackabuse.com/creating-and-deleting-directories-with-python/
    try:
        os.makedirs(dirname)
    except OSError as excpt:
        print("Creation of the directory %s failed: %s" % (dirname, excpt))
        return 1
    else:
        print("Successfully created the directory %s" % dirname)
        copyfile(
            os.path.join(config["adr_template_dir"], "template.md"),
            os.path.join(dirname, ".template.md"),
        )
        # try to find an init.md file to be used as the first ADR
        proj_init = os.path.join(config["adr_template_dir"], "init.md")
        dist_init = os.path.join(config["adr_bin_dir"], "init.md")
        if os.path.exists(proj_init):
            init_md = proj_init
        elif os.path.exists(dist_init):
            init_md = dist_init
        else:
            init_md = None
        adr_new(config, localpath, "record-architecture-decisions", src=init_md)
    return 0


# This function is used to read the .adr-dir file (written in adr_init), to determine the relative path for the
# adrs. default is /doc/adr/ .
# In order to find this file in another directory, an optional directory can be passed.
def find_alternate_dir(dir="doc/adr/"):
    directory = dir
    try:
        # open local file
        fh = open(os.path.join(dir, ".adr-dir"), "r")
        # add slash to remain compatible with 'default' /doc/adr/
        directory = fh.read().rstrip() + "/"
    except FileNotFoundError:
        None
    return directory


# adr-new
def adr_new(config, localpath, title, superseded=None, links=None, src=None):
    # start with no error; if it changes along the way, we have an error
    result = "no error"

    # location of adrs
    adr_dir = _adr_dir()

    if not src:
        # directory for the template
        src = os.path.join(_adr_dir(), ".template.md")

    # check input argument for the ADR title
    try:
        # check if title can be converted to string, and
        # replace spaces with dashes on the go
        adr_print(title)

        if type(title) == list:
            title_checked = "-".join(title).replace(" ", "-")
        elif type(title) == str:
            title_checked = title.replace(" ", "-")
    except ValueError:
        result = "Title was no string"
        print("adr-new had no valid input for the title")

    if result == "no error":
        # find highest index

        # first, find last item in adr_list
        try:
            highest_file_name = adr_list(adr_dir)[-1]
            # extract filename from path
            adr_index = int(os.path.basename(highest_file_name)[:4])
        except Exception:
            # if no valid index (for example when running adr-init),
            # make a new one
            adr_index = 0
        adr_print("adr-new; highest index = " + str(adr_index))
        # increment index for new adr
        adr_index += 1
        # Format number to string with 4 characters
        # https://stackoverflow.com/questions/11714859/how-to-display-the-first-few-characters-of-a-string-in-python
        adr_index_text = "{0:04d}".format(adr_index)

        # combine data to make destination path
        dst = os.path.join(
            adr_dir, adr_index_text + "-" + title_checked.lower() + ".md"
        )
        adr_print("adr-new; " + src + " " + dst)
        # copy template to destination directory, with correct title
        copyfile(src, dst)
        adr_write_number_and_header(dst, adr_index_text, title_checked)

        # Handle optional commands, -s and -l

        # -s

        if superseded is not None:
            for supersede in superseded:
                supersede_text = supersede[0]
                # index zero of return value of _adr_file is the number of the adr
                adr_print(
                    "adr-new; supersede_text = "
                    + supersede_text
                    + " , adr is "
                    + _adr_file(supersede_text)[1]
                )
                _adr_add_link(supersede_text, "superceded by", _adr_file(dst)[1])
                _adr_add_link(_adr_file(dst)[1], "supercedes", supersede_text)

        # -l

        # example: -l "5:Amends:Amended by"
        if links is not None:
            for linkadr in links:
                try:
                    adr_print("adr-new; linktext = " + linkadr)
                    # split by colon
                    target, link, reverse_link = linkadr.split(":")
                    # index zero of return value of _adr_file is the number of the adr
                    _adr_add_link(_adr_file(dst)[1], link, _adr_file(target)[1])
                    _adr_add_link(_adr_file(target)[1], reverse_link, _adr_file(dst)[1])
                except:
                    # error message, print even if verbosity is off
                    print("failed to process -l option. Error in argument formatting?")

    _adr_gen_index()

    return dst


# Write ADR number in filename and header
def adr_write_number_and_header(dst, adr_index, adr_title=None):
    # https://www.programiz.com/python-programming/datetime/current-datetime
    today = date.today().strftime("%Y-%m-%d")
    # open file for appending and reading and replacing
    # https://kaijento.github.io/2017/05/28/python-replacing-lines-in-file/
    for line in fileinput.input(dst, inplace=True):
        if fileinput.filelineno() == 1:
            # first replace number
            line = line.replace("NUMBER", str(int(adr_index)))
            # now add title if needed
            if adr_title is not None:
                # insert title with one capital at the start
                adr_title = "".join([adr_title[0].upper()] + list(adr_title[1:]))
                line = line.replace("TITLE", adr_title.replace("-", " "))
        else:
            line = line.replace("DATE", today)
        print(line, end="")
    fileinput.close()


# add a link to another adr
def _adr_add_link(source, linktype, target):
    source_adr = _adr_file(source)[1]
    target_adr = _adr_file(target)[1]

    adr_print(
        "_adr_add_link; source_adr = " + source_adr + " target_adr is " + target_adr
    )
    link_text = (
        linktype
        + " ["
        + _adr_title(target)
        + "]("
        + os.path.basename(target_adr)
        + ")"
    )
    # Careful! No adr_print stuff in this section, because it will end up
    # in the adr, as fileinput takes over stdout
    for line in fileinput.input(source_adr, inplace=True):
        STATUS = 'Status: '
        idx = line.find(STATUS)
        if idx != -1:
            print(line[:idx + len(STATUS)] + link_text)
        else:
            print(line, end="")
    fileinput.close()


def _adr_dir():
    newdir = dir = os.getcwd()

    # confuscated do-while
    # https://www.javatpoint.com/python-do-while-loop
    while True:
        adr_print("_adr_dir: " + dir)
        dir_docadr = os.path.join(dir, "doc/adr")
        path_adrdir = os.path.join(dir, ".adr-dir")
        if os.path.isdir(dir_docadr):
            adr_print("_adr_dir, found /doc/adr in " + dir_docadr)
            newdir = dir_docadr
            break
        elif os.path.isfile(path_adrdir):
            adrdir_directory = os.path.join(dir, find_alternate_dir(dir))
            adr_print("_adr_dir, found .adr_dir, referring to " + adrdir_directory)
            newdir = adrdir_directory
            break
        # https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        # Go up one directory
        newdir = os.path.dirname(dir)
        # If you can't go up further, you've reached the root.
        if newdir == dir:
            # default value is 'doc/adr/'
            newdir = "doc/adr/"
            break

        dir = newdir
    # original adr-tools returns relative path w.r.t path from which the function was called.
    return os.path.relpath(newdir, os.getcwd())


# adr_file returns first file that contains the text. Since list_of_adrs returns a
# sorted list, searching for the ADR number will generally yield the correct ADR.
#
def _adr_file(adr_text):
    list_of_adrs = adr_list(_adr_dir())
    # string or integer input
    if type(adr_text) is int:
        adr_text = str(adr_text)
    for adr in list_of_adrs:
        # adr_print("_adr_file; adr = " + adr)
        if adr_text in adr:
            adr_print("_adr_file; found " + adr_text + " in " + adr)
            return (int(os.path.basename(adr)[0:4]), adr)
    adr_print("_adr_file; no record found containing " + adr_text)
    return (0, "")


# adr_title returns first line of ADR, without the # and without newline at the end
def _adr_title(text):
    # adr_file returns tuple with number and string
    adr = _adr_file(text)
    adr_print(
        "_adr_title; number is "
        + str(adr[0])
        + ", adr is "
        + adr[1]
        + "path is "
        + os.getcwd()
    )
    with open(adr[1], "r") as f:
        adrline = f.readline()
        adr_print("_adr_title; line is ")
    # Strip markdown header 1 (#), and strip newline
    return adrline[2:-1]


# adr_list returns a sorted list of all ADRs
def adr_list(dir):
    adr_dir = _adr_dir()
    adr_list = list()
    adr_print("adr_list; adr directory is " + adr_dir)
    onlyfiles = [f for f in listdir(adr_dir) if isfile(join(adr_dir, f))]
    # make list of adr files. All files *not* starting with 4 numbers
    # are skipped.
    for file in onlyfiles:
        try:
            # if this fails, the 'except' will be executed, and
            # actions past this line will be skipped
            if _VALID_FILENAME_REGEXP.match(file):
                adr_list.append(file)
        except Exception:
            adr_print(file + " is not a valid ADR filename")
            None
    adr_paths = list()
    # create full path adr list
    for adr in sorted(adr_list):
        adr_paths.append(os.path.join(adr_dir, adr))
    return adr_paths


# get the title of an ADR from its path
def _adr_file_title(path):
    with open(path) as adr:
        try:
            return adr.readline().split(". ")[1].strip()
        except IndexError:
            pass
    return os.path.basename(path)


# generate an index.md from the list of ADR files
def _adr_gen_index():
    adr_dir = _adr_dir()
    with open(os.path.join(adr_dir, "index.md"), "w") as index:
        print("# Architectural Decision Records\n", file=index)
        for adr in adr_list(adr_dir):
            print(
                "* [%s](%s)" % (_adr_file_title(adr), os.path.basename(adr)), file=index
            )
