#!/bin/bash

mkdir -p logs

python wonderbot.py comments

sleep 30

python wonderbot.py submissions

