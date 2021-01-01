#!/bin/bash
find . -type f -name "*_result.csv" | xargs grep -ncr "[0-9]*[0-9],NO_PEAK,\"\[\]\",NO_PEAK,\"\[\]\",NO_PEAK,\"\[\]\",NO_PEAK,\"\[\]\"$" | grep -o "Spectro[0-9]*[0-9]_result.csv:[2-9][0-9][0-9]$" 
