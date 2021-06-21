#!/usr/bin/env bash
# Generates the documentation for the project
if [ -d "docs" ]; then
    cd "docs" || exit
fi

mkdir -p source/tmp
make clean
find source \( -name '*.svg' -o -name '*.png' -o -name '*.md' \) -exec rm {} \;

sphinx-apidoc -f -o source/ ../src/firmware
find ../ -path '../vendor' -prune  -o -path "../docs" -prune -o \( -name '*.svg' -o -name '*.png' -o -name '*.md' \)   -exec cp --parents \{\} source/tmp \;
make html
