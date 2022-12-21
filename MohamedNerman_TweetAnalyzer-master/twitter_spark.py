from pyspark import SparkConf, SparkContext                                                                                                                                                                                                                                                                                                                                                                                         
from pyspark.streaming import StreamingContext                                                                                                                                                                                                                                                                                                                                                                                      
from pyspark.streaming.kafka import KafkaUtils                                                                                                                                                                                                                                                                                                                                                                                      
from pyspark.sql import SparkSession                                                                                                                                                                                                                                                                                                                                                                                                
import os                                                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                    
sparkVersion = '2.0.0'  # update this accordingly                                                                                                                                                                                                                                                                                                                                                                                   
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:{} pyspark-shell'.format(sparkVersion)                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                    
scala_version = '2.12'                                                                                                                                                                                                                                                                                                                                                                                                              
spark_version = '2.4.6'                                                                                                                                                                                                                                                                                                                                                                                                             
# TODO: Ensure match above values match the correct versions                                                                                                                                                                                                                                                                                                                                                                        
packages = [f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',                                                                                                                                                                                                                                                                                                                                               
    'org.apache.kafka:kafka-clients:3.2.1']                                                                                                                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                                    
def main():                                                                                                                                                                                                                                                                                                                                                                                                                         
    conf = SparkConf().setMaster("local[2]").set("spark.jars.packages", ",".join(packages)).setAppName("KAFKAStreaming").set("spark.ui.port", "44040")                                                                                                                                                                                                                                                                              
    sc = SparkContext(conf=conf)                                                                                                                                                                                                                                                                                                                                                                                                    
    spark = SparkSession(sc)                                                                                                                                                                                                                                                                                                                                                                                                        
    ssc = StreamingContext(sc, 5)                                                                                                                                                                                                                                                                                                                                                                                                   
    ssc.checkpoint("checkpoint")                                                                                                                                                                                                                                                                                                                                                                                                    
    sportwords = load_wordlist("./dataset/sports.txt")                                                                                                                                                                                                                                                                                                                                                                              
    polwords = load_wordlist("./dataset/politics.txt")                                                                                                                                                                                                                                                                                                                                                                              
    muwords = load_wordlist("./dataset/music.txt")                                                                                                                                                                                                                                                                                                                                                                                  
    artswords = load_wordlist("./dataset/arts.txt")                                                                                                                                                                                                                                                                                                                                                                                 
    eduwords = load_wordlist("./dataset/education.txt")                                                                                                                                                                                                                                                                                                                                                                             
    stream(ssc, sportwords, polwords, muwords, artswords, eduwords)                                                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                    
def load_wordlist(filename):                                                                                                                                                                                                                                                                                                                                                                                                        
    words = {}                                                                                                                                                                                                                                                                                                                                                                                                                      
    f = open(filename, 'rU')                                                                                                                                                                                                                                                                                                                                                                                                        
    text = f.read()                                                                                                                                                                                                                                                                                                                                                                                                                 
    text = text.split('\n')                                                                                                                                                                                                                                                                                                                                                                                                         
    for line in text:                                                                                                                                                                                                                                                                                                                                                                                                               
        words[line] = 1                                                                                                                                                                                                                                                                                                                                                                                                             
    f.close()                                                                                                                                                                                                                                                                                                                                                                                                                       
    return words                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                    
def update_function(new_values, running_count):                                                                                                                                                                                                                                                                                                                                                                                     
    if running_count is None:                                                                                                                                                                                                                                                                                                                                                                                                       
        running_count = 0                                                                                                                                                                                                                                                                                                                                                                                                           
    return sum(new_values, running_count)                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                    
from datetime import datetime                                                                                                                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                                                                                                    
def save_to_hadoop(t, rdd):                                                                                                                                                                                                                                                                                                                                                                                                         
    print("=====Pull from Stream=====")                                                                                                                                                                                                                                                                                                                                                                                             
    if not rdd.isEmpty():                                                                                                                                                                                                                                                                                                                                                                                                           
        now = datetime.now()                                                                                                                                                                                                                                                                                                                                                                                                        
        current_time = now.strftime("%H:%M:%S")                                                                                                                                                                                                                                                                                                                                                                                     
        hour = now.strftime("%H")                                                                                                                                                                                                                                                                                                                                                                                                   
        print("=some records=")                                                                                                                                                                                                                                                                                                                                                                                                     
        rdd=rdd.map(lambda x: (x[0],x[1],str(current_time),str(hour)))                                                                                                                                                                                                                                                                                                                                                              
        print(str(t))                                                                                                                                                                                                                                                                                                                                                                                                               
        print(rdd.collect())                                                                                                                                                                                                                                                                                                                                                                                                        
        df = rdd.toDF().withColumnRenamed("_1", "theme").withColumnRenamed("_2", "count").withColumnRenamed("_3", "time").withColumnRenamed("_4", "hour")                                                                                                                                                                                                                                                                           
        df.printSchema()                                                                                                                                                                                                                                                                                                                                                                                                            
        spark = SparkSession.builder.getOrCreate                                                                                                                                                                                                                                                                                                                                                                                    
        df.write.format("parquet").mode("append").save("/user/spark/test")                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                                                    
def stream(ssc, sportwords, polwords, muwords, artswords, eduwords):                                                                                                                                                                                                                                                                                                                                                                
    kstream = KafkaUtils.createDirectStream(                                                                                                                                                                                                                                                                                                                                                                                        
        ssc, topics=['TweetsTopicss'], kafkaParams={"metadata.broker.list":'sandbox-hdp.hortonworks.com:6667'})                                                                                                                                                                                                                                                                                                                     
    kstream.map(lambda x: print( x[1].encode("utf8", "ignore")))                                                                                                                                                                                                                                                                                                                                                                    
    tweets = kstream.map(lambda x: x[1].encode("utf8", "ignore"))                                                                                                                                                                                                                                                                                                                                                                   
    words = tweets.flatMap(lambda line: str(line).split(" "))                                                                                                                                                                                                                                                                                                                                                                       
    sports = words.map(lambda word: ('Sports', 1) if word in sportwords else ('Sports', 0))                                                                                                                                                                                                                                                                                                                                         
    politics = words.map(lambda word: ('Politics', 1) if word in polwords else ('Politics', 0))                                                                                                                                                                                                                                                                                                                                     
    art = words.map(lambda word: ('Art', 1) if word in artswords else ('Art', 0))                                                                                                                                                                                                                                                                                                                                                   
    music = words.map(lambda word: ('Music', 1) if word in muwords else ('Music', 0))                                                                                                                                                                                                                                                                                                                                               
    education = words.map(lambda word: ('Education', 1) if word in eduwords else ('Education', 0))                                                                                                                                                                                                                                                                                                                                  
    all_sentiments = sports.union(politics).union(art).union(music).union(education)                                                                                                                                                                                                                                                                                                                                                
    sentiment_counts = all_sentiments.reduceByKey(lambda x, y: x + y)                                                                                                                                                                                                                                                                                                                                                               
    running_sentiment_counts = sentiment_counts.updateStateByKey(update_function)                                                                                                                                                                                                                                                                                                                                                   
    running_sentiment_counts.pprint()                                                                                                                                                                                                                                                                                                                                                                                               
    sentiment_counts.foreachRDD(save_to_hadoop)                                                                                                                                                                                                                                                                                                                                                                                     
    ssc.start()                                                                                                                                                                                                                                                                                                                                                                                                                     
    ssc.awaitTermination()                                                                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                    
if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                                          
    main()