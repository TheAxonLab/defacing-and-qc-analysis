# !! To run this script, you need to have run docker-compose up in the qkay repository to have running containers !!

import pandas as pd
from pymongo.mongo_client import MongoClient

# Path PyMongo to allow using PyMongoArrow’s functionality directly to Collection instances of PyMongo
from pymongoarrow.monkey import patch_all 
patch_all()

# Connect to the MongoDB database
client = MongoClient('localhost', 27017)
                          
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# List available databases
database_names = client.list_database_names()
for db_name in database_names:
    print(db_name)

# Select the database and extract all ratings
db = client.data_base_qkay
ratings = db.ratings
df = ratings.find_pandas_all({"dataset": "IXI dataset - MRIQC derivatives"})

# Replace newline characters in the 'comments' column with a space
# so that comments do not get split into multiple lines
df["comments"] = df["comments"].str.replace("\n", ", ")

#Drop columns we don't need
df = df.drop(columns = ['_id', 'md5sum'])

# Save dataframe to csv so we can load it in R
df.to_csv('IXI_ratings_df.csv')

# Close the connection
client.close()
