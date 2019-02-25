# Copy data/WineNewGBTDataSet.csv to hadoop user homedir

!hadoop fs -rm -skipTrash NewGBTDataSet.csv
!hadoop fs -put data/NewGBTDataSet.csv
!pip3 install --upgrade pip 
!pip3 install seaborn