import sqlite3 

## Connectig to SQLite
connection = sqlite3.connect("student.db")

# Create a cursor object to insert records, create table

cursor= connection.cursor()

# Create the table
table_info="""
Create table STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT); 

"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''Insert into STUDENT values('Sahil','Data analyst','A', 90)''')
cursor.execute('''Insert into STUDENT values('Raj','Data analyst','A',80)''')
cursor.execute('''Insert into STUDENT values('Om','Software Engineering','B',50)''')
cursor.execute('''Insert into STUDENT values('Sarthak','Data analyst','A',82)''')
cursor.execute('''Insert into STUDENT values('Tanmay','Software engineering','B',70)''')

# Displays all records in terminal
print("The inserted records are")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
    
# Commit changes in database
connection.commit()
connection.close() 