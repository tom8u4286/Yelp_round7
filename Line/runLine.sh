
for i in ../data/line-data/cooccurrence/restaurant_1_cooccur.txt
do
    echo "Running Line (first-order) on:\033[1m" $i "\033[0m"
    filename=$(echo $i | cut -d'/' -f 5)
    num=$(echo $filename | egrep -o "[0-9]+")
    echo $num
    #echo $filename
    ts -n -f sh -c "./line -train $i -output ../data/line-data/vectors/200dim/restaurant_"$num"_vector200.txt -size 200 -order 1 -negative 5 -samples 1 -threads 1
    ./normalize -input ../data/line-data/vectors/200dim/restaurant_"$num"_vector200.txt -output ../data/line-data/vectors/norm_200dim/norm_restaurant_"$num"_vector2.txt -binary 0
    #" 
    echo "-------------------------------------------"
done    
#ts -S 20
