#First we import the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
np.set_printoptions(suppress = True, linewidth = 100, precision = 2)

#Finding the path of the file with a function
def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)
   print(file_path)

   return file_path


#Then we import our data
#Viewing the raw data
#raw_data_np = np.genfromtxt(open_file_in_same_directory("Absenteeism-data.csv"), delimiter = ";",skip_header= 1, autostrip= True)
#print(raw_data_np)
raw_csv_data = pd.read_csv(open_file_in_same_directory("Absenteeism-data.csv"))
print(raw_csv_data)
#Copying the data for safety
df = raw_csv_data.copy() #We now work with the df as our data

#Step 1: Drop the ID column
df=df.drop('ID',
  axis='columns')

#df = df.drop(['ID'], axis = 1)

print(df)
#From the info method, we can see that there are no missing values
print(df.info())


#Step 2: Split the reasons for absence into multiple dummy variables, and then group them in the following way:
#Group 1: Columns 1 to 14
#Group 2: Columns 15, 16, and 17
#Group 3: Columns 18, 19, 20, and 21
#Group 4: Columns 22 to 28

#Reasons for absence
#Checking the unique values
print(sorted((df['Reason for Absence'].unique())))
#We can see that there are 28 unique values. But the 20 value is missing.
#The reasons from 0 to 28 have a meaning depending on the number of the reason. Based on the exercise we have to group them into 4 categories.
#Lets create dummy variables for the reason of absence
reason_columns = pd.get_dummies(df['Reason for Absence'])
# reason_columns

#Here we check if the sum of each column is equal to 1
#It should be 1 because, the exercise states that there can be only 1 reason for absence at a time.
reason_columns['check'] = reason_columns.sum(axis=1)
# reason_columns
#It's correct but its not enough. We can check the sum of the check column to see how many rows there are. If it's 700 we are correct.
# reason_columns['check'].sum(axis=0)
#The sum is 700 but it's not enough yet. How do we know if the sum is 700 but for a different reason? For example, a wrong sum.
#With the unique method we can check if the only variable is 1.
# reason_columns['check'].unique()
#We are correct. This means that we have succesfully created a dummie table for the reason of absence.
#Now we have to drop the check column
reason_columns = reason_columns.drop(['check'], axis = 1)
# reason_columns
#We drop the first reason of absence (0) so we don't get confused in a later stage. (Multicollinearity)
reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first = True)
# reason_columns

#We drop the reason of absence column in order to manipulate it
df = df.drop(['Reason for Absence'], axis = 1)
# df

#The max portion of the code indicates that if the result is 0, the reason is not in the group category. If it's 1, it is.
reason_type_1 = reason_columns.loc[:, 1:14].max(axis=1)
reason_type_2 = reason_columns.loc[:, 15:17].max(axis=1)
reason_type_3 = reason_columns.loc[:, 18:21].max(axis=1)
reason_type_4 = reason_columns.loc[:, 22:].max(axis=1)

#Concatenating the columns
df = pd.concat([df, reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis = 1)
# df

# df.columns.values
column_names = ['Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours', 'Reason_1', 'Reason_2', 'Reason_3', 'Reason_4']

df.columns = column_names

#Reordering the columns
column_names_reordered = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 
                          'Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']

df = df[column_names_reordered]

#Checkpoint
df_reason_mod = df.copy()

#Date column
#Changing the date format, because some Dates were not correctly formatted.
df_reason_mod['Date'] = pd.to_datetime(df_reason_mod['Date'], format = '%d/%m/%Y')

#Extracting the month value
list_months = []

for i in range(df_reason_mod.shape[0]):
    list_months.append(df_reason_mod['Date'][i].month)
    
df_reason_mod['Month Value'] = list_months

#Creating a day of the week column
#Creating a function for 1 element, so we can use it for every element later.
def date_to_weekday(date_value):
    return date_value.weekday()

df_reason_mod['Day of the Week'] = df_reason_mod['Date'].apply(date_to_weekday)

df_reason_mod = df_reason_mod.drop(['Date'], axis = 1)

column_names_upd = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value', 'Day of the Week',
       'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education', 'Children',
       'Pets', 'Absenteeism Time in Hours']
df_reason_mod = df_reason_mod[column_names_upd]


#Checkpoint
df_reason_date_mod = df_reason_mod.copy()

#Education column
#We are changing the education column from 1-4 to 0 or 1. The value 0 means they only went to high school, while 1 means they have a higher form of education.
df_reason_date_mod['Education'] = df_reason_date_mod['Education'].map({1:0, 2:1, 3:1, 4:1})

#Final checkpoint
df_cleaned = df_reason_date_mod.copy()
print(df_cleaned.head(10))