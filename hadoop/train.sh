hadoop dfs -rm -r /user/nidhinkrishnanv/train

hadoop jar hadoop-streaming.jar \
-file ./mapper.py -mapper ./mapper.py \
-file ./reducer.py -reducer ./reducer.py \
-input /user/ds222/assignment-1/DBPedia.verysmall/verysmall_train.txt -output /user/nidhinkrishnanv/train

rm -rf output

hadoop dfs -copyToLocal /user/nidhinkrishnanv/train .