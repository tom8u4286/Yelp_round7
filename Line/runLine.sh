
for i in ../data/line-data/cooccurrence/restaurant_*_cooccur.txt
#for i in restaurant_*_cooccur.txt 
do
    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
    filename=$(echo $i | cut -d'/' -f 5)
    echo $filename
    ts -n -f sh -c "./line -train $i -output ../data/line-data/vectors/200dim/$filename -size 100 -order 1 -negative 5 -samples 10 -threads 1
    #./line -train $i -output ../data/line-data/vectors/200dim/$filename -size 200 -order 1 -negative 5 -samples 10 -threads 5
    echo $filename
    ./normalize -input ../data/line-data/vectors/200dim/$filename -output ../data/line-data/vectors/norm_200dim/norm_$filename -binary 0
    " &
    echo "-------------------------------------------"
done    
ts -S 20
