source /etc/profile
source ~/.bashrc
YESTERDAY_DT=`date +'%Y%m%d' -d "-1day"`
TODAY_DT=`date +'%Y%m%d'`
INPUT_DIR_INC=/ad/zhanqun/database/corpora/inc/${YESTERDAY_DT}
INPUT_DIR_ALL=/ad/zhanqun/database/corpora/all/${YESTERDAY_DT}
OUTPUT_DIR=/ad/zhanqun/database/corpora/all/${TODAY_DT}
hls $INPUT_DIR_ALL
if [ $? -ne 0 ];then
    echo 'yesterday all data content is not exist, please check!'
    exit 1
fi
hls $INPUT_DIR_INC
if [ $? -ne 0 ];then
    hcp $INPUT_DIR_ALL/* $OUTPUT_DIR
    echo 'yesterday inc data content is not exist, cp yesterday files'
    exit 0
fi

$HADOOP_HOME/bin/hadoop fs -rmr $OUTPUT_DIR
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar \
    -input $INPUT_DIR_INC \
    -input $INPUT_DIR_ALL \
    -output $OUTPUT_DIR \
    -mapper ./mapper.py \
    -file ./mapper.py \
    -numReduceTasks 500 \
    -reducer ./reducer.py \
    -file ./reducer.py
