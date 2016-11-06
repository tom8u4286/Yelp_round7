#!/bin/zsh

for i in data/reviews/*.json
do
    ts -n -f sh -c "python StarRepresentationTest.py $i" &
done
ts -S 20
