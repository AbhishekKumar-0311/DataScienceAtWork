# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ### Prepared by Abhishek Kumar
# ### https://www.linkedin.com/in/abhishekkumar-0311/
#

# # Writing SQL query on a dataframe using pandassql

# +
# To get multiple outputs in the same cell

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# %matplotlib inline

# +
# #!pip install pandasql

import pandas as pd
import numpy as np
import pandasql as ps
from pandasql import sqldf
import sqlite3
from sqlite3 import Error

df = pd.read_csv('E:\VCS\GitHub\Machine-Learning-with-Python\data\movie.csv')

df.head()

# +
# #%%timeit
pysqldf = lambda q: sqldf(q, globals())

q1 = "Select * from df where director_name = 'James Cameron'"
pysqldf(q1)

q2 = "Select director_name , sum(num_critic_for_reviews) as tot_critic from df group by director_name order by tot_critic desc"
pysqldf(q2)#.sort_values(by=)
pysqldf(q2).sort_values(by='tot_critic', ascending=True)
# -

# ### https://www.kdnuggets.com/2017/02/python-speak-sql-pandasql.html

# # SQLite Python

# ### https://datatofish.com/create-database-python-using-sqlite3/#:~:text=Import%20the%20CSV%20files%20using,file%20using%20the%20to_csv%20command

# +
import sqlite3

conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - CLIENTS
c.execute('''CREATE TABLE CLIENTS
             ([generated_id] INTEGER PRIMARY KEY,[Client_Name] text, [Country_ID] integer, [Date] date)''')
          
# Create table - COUNTRY
c.execute('''CREATE TABLE COUNTRY
             ([generated_id] INTEGER PRIMARY KEY,[Country_ID] integer, [Country_Name] text)''')
        
# Create table - DAILY_STATUS
c.execute('''CREATE TABLE DAILY_STATUS
             ([Client_Name] text, [Country_Name] text, [Date] date)''')
                 
conn.commit()

# Note that the syntax to create new tables should only be used once in the code (unless you dropped the table/s at the end of the code). 
# The [generated_id] column is used to set an auto-increment ID for each record
# When creating a new table, you can add both the field names as well as the field formats (e.g., Text)
# -







# +
import sqlite3
import pandas as pd
from pandas import DataFrame

conn = sqlite3.connect('movie.db')  
c = conn.cursor()

movie = pd.read_csv (r'E:\VCS\GitHub\Machine-Learning-with-Python\data\movie.csv')
movie.to_sql('MOVIE', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 

read_country = pd.read_csv (r'C:\Users\Ron\Desktop\Client\Country_14-JAN-2019.csv')
read_country.to_sql('COUNTRY', conn, if_exists='replace', index = False) # Replace the values from the csv file into the table 'COUNTRY'

# When reading the csv:
# - Place 'r' before the path string to read any special characters, such as '\'
# - Don't forget to put the file name at the end of the path + '.csv'
# - Before running the code, make sure that the column names in the CSV files match with the column names in the tables created and in the query below
# - If needed make sure that all the columns are in a TEXT format

c.execute('''
INSERT INTO DAILY_STATUS (Client_Name,Country_Name,Date)
SELECT DISTINCT clt.Client_Name, ctr.Country_Name, clt.Date
FROM CLIENTS clt
LEFT JOIN COUNTRY ctr ON clt.Country_ID = ctr.Country_ID
          ''')

c.execute('''
SELECT DISTINCT *
FROM DAILY_STATUS
WHERE Date = (SELECT max(Date) FROM DAILY_STATUS)
          ''')
   
#print(c.fetchall())

df = DataFrame(c.fetchall(), columns=['Client_Name','Country_Name','Date'])
print (df) # To display the results after an insert query, you'll need to add this type of syntax above: 'c.execute(''' SELECT * from latest table ''')

df.to_sql('DAILY_STATUS', conn, if_exists='append', index = False) # Insert the values from the INSERT QUERY into the table 'DAILY_STATUS'

# export_csv = df.to_csv (r'C:\Users\Ron\Desktop\Client\export_list.csv', index = None, header=True) # Uncomment this syntax if you wish to export the results to CSV. Make sure to adjust the path name
# Don't forget to add '.csv' at the end of the path (as well as r at the beg to address special characters)
# -



# ## https://www.sqlitetutorial.net/sqlite-python/create-tables/

# When you connect to an SQLite database file that does not exist, SQLite automatically creates the new database for you.
#
# To create a database, first, you have to create a Connection object that represents the database using the connect() function of the sqlite3 module.
#
# For example, the following Python program creates a new database file pythonsqlite.db in the c:\sqlite\db folder.
#
# Note that you must create the c:\sqlite\db folder first before you execute the program. Or you can place the database file a folder of your choice.
#
#

# +
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"E:\VCS\GitHub\Machine-Learning-with-Python\data\movie.db")
# -

# In this code:
#
# First, we define a function called create_connection() that connects to an SQLite database specified by the database file db_file. Inside the function, we call the connect() function of the sqlite3 module.
#
# The connect() function opens a connection to an SQLite database. It returns a Connection object that represents the database. By using the Connection object, you can perform various database operations.
#
# In case an error occurs, we catch it within the try except block and display the error message. If everything is fine, we display the SQLite database version.
#
# It is a good programming practice that you should always close the database connection when you complete with it.
#
# Second, we pass the path of the database file to the create_connection() function to create the database. Note that the prefix r in the  r"E:\VCS\GitHub\DataScienceAtWork\data\movie.db" instructs Python that we are passing a raw string.
#
# Let’s run the program and check the E:\VCS\GitHub\DataScienceAtWork\data folder.
#
# python sqlite create database
# If you skip the folder path E:\VCS\GitHub\DataScienceAtWork\data, the program will create the database file in the current working directory (CWD).
#
# If you pass the file name as :memory: to the connect() function of the sqlite3 module, it will create a new database that resides in the memory (RAM) instead of a database file on disk.





# +
import pymysql
import pandas as pd

# Create dataframe
data = pd.DataFrame({
    'Capital':["Kolkata", "Hyderabad", "Bengaluru"],
    'Founded':['1596', '1561', '1537'],
    'Address':['WB','TS','KA']
})


# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='mydb')


# create cursor
cursor=connection.cursor()

# creating column list for insertion
cols = "`,`".join([str(i) for i in data.columns.tolist()])

# Insert DataFrame recrds one by one.
for i,row in data.iterrows():
    sql = "INSERT INTO `city` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))

    # the connection is not autocommitted by default, so we must commit to save our changes
    connection.commit()

# Execute query
sql = "SELECT * FROM `city`"
cursor.execute(sql)

# Fetch all the records
result = cursor.fetchall()
for i in result:
    print(i)

connection.close()

 

# Note :-

# My table description

# describe city;

# # +---------+--------------+------+-----+---------+----------------+

# | Field   | Type         | Null | Key | Default | Extra          |

# # +---------+--------------+------+-----+---------+----------------+

# | ID      | int          | NO   | PRI | NULL    | auto_increment |

# | Capital | varchar(255) | YES  |     | NULL    |                |

# | Founded | varchar(255) | YES  |     | NULL    |                |

# | Address | varchar(255) | YES  |     | NULL    |                |

# # +---------+--------------+------+-----+---------+----------------+


# -


