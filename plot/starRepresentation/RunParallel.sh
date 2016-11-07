#!/bin/zsh

for i in ../../data/reviews_each_with_stars/*.json
do
    ts -n -f sh -c "python StarRepresentationTest.py $i" &
done
ts -S 20

echo "All process completed."
