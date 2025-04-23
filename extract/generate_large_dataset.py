from faker import Faker # python library to generate fake records (Amazon products)
import random           # built-in python module to pick random values like categories,price,date,etc..
import pandas as pd     # using pandas to convert fake data into dataset then save it as a JSON file.

fake = Faker()          # creates a faker object to generate fake values.
categories = ["Electronics", "Clothing", "Books", "Home", "Beauty", "Toys"] #List of sample products to randomly assign.
num_records = 500000    # number of records we want to generate.

def create_products():
    return{
        "product_id" : fake.uuid4(), # uuid is unique id 4 means version 4.
        "title" : fake.catch_phrase(), # any marketing phrase.
        "category" : random.choice(categories),
        "price" : round(random.uniform(10,1000),2),
        "rating" : round(random.uniform(1,5),1),
        "review_count" : random.randint(0,5000),
        "availability" : random.choice(["In Stock", "Out of Stock", "Limited Stock"]),
        "timestamp" : fake.iso8601()
    }

def generate_data():

    print("Creating records............") # just to see if the program is working

    data=[create_products() for _ in range(num_records)] # to store all records in list by using loop

    df=pd.DataFrame(data)   # convert the randomly created data's list in pandas dataframe

    df.to_json("/opt/airflow/output/large_raw_data.json", orient="records", lines=True)
    # convert the dataframe into json format and save it in the given location
    # orient means saves each row as a separate json object.
    # line means Makes it new-line delimited:- saves as one json object per line.


    print(f"successfully created {num_records} at 'large_raw_data.json'")

if __name__ == "__main__":
    generate_data()