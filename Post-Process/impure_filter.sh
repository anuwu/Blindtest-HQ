#!/bin/bash

cat $1 | grep -v "[0-9]*,,,"
rm -i $1
