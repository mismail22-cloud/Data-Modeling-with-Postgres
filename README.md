# purpose of this database in the context of the startup, Sparkify, and their analytical goals:
On a high level, this Database aims to serve Sparkify for getting analytical figures for their Music store.
The analytical figures help Sparkify to increase their sales and know better their customer and users and the top requested songs and artists as well as categorizing their users by knowing the type of favourite songs and prefered artists for each user.

# Below are examples for analytical figures that would be very useful and is easy to be got from this Database:
1- Top ranked songs that were listened to per month
2- Top ranked songs that were listened to per year
3- Top ranked artists that were listened to per month
4- Top ranked artists that were listened to per year
5- Revenue breakdown by artists and songs 
6- Average Revenue per User
7- Top ranked Users by their payments (on Daily Basis ,Month basis or Yearly Basis)
8- Know how tight is the relation of the user's location to his top ranked artist location
9- Top ranked Songs and artists for male users 
10-Top ranked Songs and artists for Female users
11-Know the top ranked songs duration and dig deeper if the Song duration affects the Song rank  

# Database schema design and ETL pipeline:
## Database schema
The Database is a dimensional Star Schema Database that consists of one Fact table "songplays" surrounded by denormalized dimensions "Users","Songs","Artists","Time".
This design serves dynamic analytical queries to be run on the model as well as changing this Ad-hoc queries if required.It also serves fast reads as it is denormalized so the data retrieval is very fast.

## ETL pipeline
The ETL is done by two Python Scripts , First one is to prepare the tables and DB Schema.This Drops the tables if exists and then create all the tables.
The second Script is the actual extraction of Data from the JSON files and doing the required Transformation and then loading to the Database tables.
This ETL is so effecient and it can be enhanced by using Bulk Loads instead of normal inserts.
The ETL process Start filling the Dimension tables and ends with populating the Fact table so that to be able to get the IDs from the already loaded dimensions and inject them in the Fact table records.
