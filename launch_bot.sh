#!/bin/bash

mkdir -p logs

nohup python wonderbot.py comments > logs/comments_nohup.out 2> logs/comments_nohup.err &

sleep 30

nohup python wonderbot.py submissions > logs/submissions_nohup.out 2> logs/submissions_nohup.err &

