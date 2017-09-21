export REDUCERS=$1

hadoop dfs -rm -r /user/nidhinkrishnanv/request

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./request_mapper.py -mapper ./request_mapper.py \
-file ./request_reducer.py -reducer ./request_reducer.py \
-input /user/ds222/assignment-1/DBPedia.full/full_test.txt,/user/nidhinkrishnanv/word/ \
 -output /user/nidhinkrishnanv/request

# rm -rf request

# hadoop dfs -copyToLocal /user/nidhinkrishnanv/request .


hadoop dfs -rm -r /user/nidhinkrishnanv/test

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./test_mapper.py -mapper ./test_mapper.py \
-file ./test_reducer.py -reducer ./test_reducer.py \
-cacheFile './cache/part-00000#cf' \
-input /user/ds222/assignment-1/DBPedia.full/full_test.txt,/user/nidhinkrishnanv/request  \
 -output /user/nidhinkrishnanv/test

rm -rf test

hadoop dfs -copyToLocal /user/nidhinkrishnanv/test .

cp -rf test/ log_files/$REDUCERS