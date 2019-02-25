
!hadoop fs -rm -skipTrash NewGBTDataSet.csv
!hadoop fs -put data/NewGBTDataSet.csv
# copied data/WineNewGBTDataSet.csv to user homedir

!pip install seaborn