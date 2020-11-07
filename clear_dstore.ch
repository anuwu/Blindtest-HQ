#!/bin/bash
# Finds '.DS_Store' files in the repository and deletes them

find . -type f -name ".DS_Store" | xargs rm
