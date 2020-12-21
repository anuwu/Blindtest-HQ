#!/bin/bash

./check.sh | grep -v "1001" | grep -o "/Spectro[0-9]*/"
