
for i in ../data/backend_reviews/restaurant_*.txt
do
    ts -n -f sh -c "python glove.py $i" &
done
ts -S 17
