#!/usr/bin/env bash

#set -x
export NO_PROFILE=yes
test "0" == "$xtrace" && set +x
. ~/.profile >/dev/null 2>&1
. ${RC_DIR}/python.rc #>/dev/null 2>&1
test 0 -ne $? && exit 1
#cd .
test -f .python-version && pyenv activate $(cat .python-version)
#echo $PATH
#pyenv version
#pip list
#pyenv which coverage

rm -fr .pytest_cache test/__pycache__ 2>/dev/null
BRANCH=0 coverage run -m pytest test --strict --timeout 30 -vv -o cache_dir=/tmp/cache
echo "\$?==$?"
BRANCH=0 coverage report
echo "\$?==$?"
