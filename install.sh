#!/bin/bash

### This file installs all required dependencies


while read p; do
  echo p
  pip install $p -t .
done <requirements.txt