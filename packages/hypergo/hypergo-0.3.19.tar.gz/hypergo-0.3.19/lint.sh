#!/bin/bash

# cp ./lint ./.git/hooks/pre-commit

mod=${1:-./hypergo}
# mod=${mod//\./\/}

# printf "\e[1mVerifying version change $mod ...\e[0m\n"
# VERSION="$(python3 -m src.version)"
# if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\n%s\e[0m\n" "$VERSION" ; exit 1; } fi

printf "\e[1mFormatting code (autopep) $mod ...\e[0m\n"
autopep8 --in-place --aggressive --aggressive --recursive $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mFormatting code (black) $mod ...\e[0m\n"
black -S --line-length 120 $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mSorting imports (isort) $mod ...\e[0m\n"
isort $mod/*.py
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mLinting (pylint) $mod ...\e[0m\n"
# find $mod -iname "*.py" | xargs pylint -d too-few-public-methods -d missing-docstring -d unused-argument -d no-self-use -d unused-variable -d line-too-long
find $mod -iname "*.py" | xargs pylint --check-quote-consistency y -d too-few-public-methods -d missing-docstring -d unused-argument -d unused-variable -d line-too-long
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mLinting (flake8) $mod ...\e[0m\n"
# flake8 --ignore=E501 --use-flake8-tabs $mod
flake8 --ignore=E501 $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mAssessing style (pycodestyle) $mod ...\e[0m\n"
pycodestyle --ignore=E501 --first $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mType Checking (mypy) $mod ...\e[0m\n"
mypy --strict  --implicit-reexport --explicit-package-bases --ignore-missing-imports $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mComplexity check $mod ...\e[0m\n"
xenon --max-absolute A --max-modules A --max-average A $mod
# if [ $? -ne 0 ]; then { printf "\e[33mWarning.\e[0m\n" ; } fi
# xenon --max-absolute B --max-modules A --max-average A $mod
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

printf "\e[1mUnit Tests (unittest) $mod ...\e[0m\n"
coverage run -m unittest discover -s tests
coverage report
if [ $? -ne 0 ]; then { printf "\e[31mFailed, aborting.\e[0m\n" ; exit 1; } fi

# cat > ./.git/hooks/post-commit<< EOF
# printf "\e[1mgit push\e[0m\n"
# git push
# printf "\e[1mgit tag %s\e[0m\n" "$VERSION"
# git tag "$VERSION"
# if [ $? -ne 0 ]; then { printf "\e[31mError tagging version %s\e[0m\n" "$VERSION" ; } fi
# printf "\e[1mgit push --tags\e[0m\n"
# git push --tags
# if [ $? -ne 0 ]; then { printf "\e[31mError tagging version %s\e[0m\n" "$VERSION" ; } fi
# printf "\e[32mSuccess.\e[0m\n"
# EOF
# chmod +x ./.git/hooks/post-commit

# printf "\e[32mSuccess.\e[0m\n"
