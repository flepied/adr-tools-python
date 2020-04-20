#!/bin/bash

set -e

cleanup() {
    cd $top
    rm -rf "$dir" $top/.adr-dir
    if [ -f $top/.adr-dir.old ]; then
        mv $top/.adr-dir.old $top/.adr-dir
    fi
}

top=$(cd $(dirname $0); pwd)
cd $top

if [ -f .adr-dir ]; then
    mv .adr-dir .adr-dir.old
fi

dir=$(mktemp -d)

echo "$dir"

test -n "$dir" -a -d "$dir"
trap cleanup 0

set -x

adr-init "$dir/adr"
adr-new Use MySQL Database
adr-new -s 2 Use PostgreSQL Database
adr-new -l "1:amends:amended by" Use MADR v2

set +x

ls -la $dir/adr

for f in $dir/adr/*.md; do
    echo
    echo $(basename $f)
    head -5 $f
done

cd $dir/adr

set -x

test -r .template.md
test -r index.md
# 4 adr lines + 2 lines for the title
test $(wc -l index.md|cut -f1 -d' ') -eq 6
test -r 0001-record-architecture-decisions.md
test -r 0002-use-mysql-database.md
test -r 0003-use-postgresql-database.md
test -r 0004-use-madr-v2.md

grep -q 'amended by' $dir/adr/0001-record-architecture-decisions.md
grep -q 'superceded by' $dir/adr/0002-use-mysql-database.md
grep -q 'supercedes' $dir/adr/0003-use-postgresql-database.md
grep -q 'amends' $dir/adr/0004-use-madr-v2.md

# tests.sh ends here
