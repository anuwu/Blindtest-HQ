#!/bin/bash
# Not working as expected

diff --new-line-format="" --unchanged-line-format="" <(printf "$1" | sort) <(printf "$2" | sort)
