export REDUCERS=$1

hadoop dfs -rm -r /user/nidhinkrishnanv/event_counts

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./count_mapper.py -mapper ./count_mapper.py \
-file ./count_reducer.py -reducer ./count_reducer.py \
-input /user/ds222/assignment-1/DBPedia.full/full_train.txt -output /user/nidhinkrishnanv/event_counts

# rm -rf event_counts

# # hadoop dfs -copyToLocal /user/nidhinkrishnanv/event_counts .


# # # ################### Count by Word ###################

hadoop dfs -rm -r /user/nidhinkrishnanv/word

hadoop jar hadoop-streaming.jar -D mapred.reduce.tasks=$REDUCERS \
-file ./word_mapper.py -mapper ./word_mapper.py \
-file ./word_reducer.py -reducer ./word_reducer.py \
-input /user/nidhinkrishnanv/event_counts/ -output /user/nidhinkrishnanv/word

# rm -rf word

# hadoop dfs -copyToLocal /user/nidhinkrishnanv/word .

################### Create cache ###################


hadoop dfs -rm -r /user/nidhinkrishnanv/cache

hadoop jar hadoop-streaming.jar \
-file ./cache_map.py -mapper ./cache_map.py \
-file ./cache_reducer.py -reducer ./cache_reducer.py \
-input /user/nidhinkrishnanv/event_counts -output /user/nidhinkrishnanv/cache

# rm -rf cache

# hadoop dfs -copyToLocal /user/nidhinkrishnanv/cache .