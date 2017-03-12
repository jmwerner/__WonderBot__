#!/bin/bash

mkdir -p logs

python wonderbot.py comments > logs/comments_nohup.out

sleep 30

python wonderbot.py submissions > logs/submissions_nohup.out

