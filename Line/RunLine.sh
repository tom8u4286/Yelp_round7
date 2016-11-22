
#for i in ../data/line-data/cooccurrence/restaurant_199_cooccur.txt
for i in ubud.txt 
do
    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
    filename=$(echo $i | cut -d'/' -f 4)
    echo $i
    ./line -train $i -output data/line-data/vectors/200dim/$i -size 200 -order 1 -negative 5 -samples 10 -threads 5
    ./normalize -input data/line-data/vectors/200dim/$i -output data/line/norm_200dim/$filename -binary 0
    echo "-------------------------------------------"
done    

