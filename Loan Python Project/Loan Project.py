import numpy as np
import os
np.set_printoptions(suppress = True, linewidth = 100, precision = 2)

#Finding the path of the file with a function
def open_file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)
   print(file_path)

   return file_path
#Viewing the raw data
raw_data_np = np.genfromtxt(open_file_in_same_directory("loan-data.csv"), delimiter = ";",skip_header= 1, autostrip= True)
print(raw_data_np)

#Checking the number of missing values (nan)
print(np.isnan(raw_data_np).sum())

#First variable will be the filler for the missing entries
#Second variable is the mean of the columns
temporary_fill = np.nanmax(raw_data_np) + 1
temporary_mean = np.nanmean(raw_data_np, axis = 0)

#Filling the missing values
temporary_stats = np.array([np.nanmin(raw_data_np, axis = 0), temporary_mean, np.nanmax(raw_data_np, axis = 0)])

#Splitting the columns into strings and numeric values
columns_strings = np.argwhere(np.isnan(temporary_mean)).squeeze()
columns_numeric = np.argwhere(np.isnan(temporary_mean)==False).squeeze()
print(columns_numeric)
#Re-importing the data set
#String data set
loan_data_strings = np.genfromtxt(open_file_in_same_directory("loan-data.csv"), delimiter = ";", skip_header = 1, autostrip = True, usecols = columns_strings, dtype = str)
print(loan_data_strings)
#Numeric data set
loan_data_numeric = np.genfromtxt(open_file_in_same_directory("loan-data.csv"), delimiter = ";", skip_header = 1, autostrip = True, usecols = columns_numeric, filling_values=temporary_fill)
print(loan_data_numeric)

#Name of the columns
header_full = np.genfromtxt(open_file_in_same_directory("loan-data.csv"), delimiter = ";", skip_footer = raw_data_np.shape[0], autostrip = True, dtype = str)
print(header_full)

header_strings, header_numeric = header_full[columns_strings], header_full[columns_numeric]
print(header_strings)
print(header_numeric)


#Creating checkpoints for safety
def checkpoint(file_name, checkpoint_header, checkpoint_data):
   np.savez(file_name, header = checkpoint_header, data = checkpoint_data)
   checkpoint_variable = np.load(file_name + ".npz")
   return checkpoint_variable
  
checkpoint_test = checkpoint("checkpoint-test", header_strings, loan_data_strings)
#Viewing the checkpoint header variable
print(checkpoint_test['header'])
#Checking if the checkpoint data set is equal with the original data set
print(np.array_equal(checkpoint_test['data'], loan_data_strings))

#Manipulating the columns values

#Issue date
loan_data_strings[:,0]=np.chararray.strip(loan_data_strings[:,0], "-15")

#Changing months strings into integer for better data analysis
months= np.array(['','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
for i in range(13):
   loan_data_strings[:,0]=np.where(loan_data_strings[:,0] == months[i], i, loan_data_strings[:,0])

#Loan Status
#  Changing the values into more simple values such as "good" or "bad" depending on their meaning
status_bad=np.array(["","Charged Off", "Default", "Late (31-120 days)"]) 
loan_data_strings[:,1]= np.where(np.isin(loan_data_strings[:,1], status_bad), 0, 1)

#Term
#First we strip the months string from the value
loan_data_strings[:,2]=np.chararray.strip(loan_data_strings[:,2], " months")
#Now we have to rename the header into term_months for better understanding of the data
header_strings[2]="term_months"
#Now we assign the missing values as 60 because its the worst possible outcome in that data column
loan_data_strings[:,2]=np.where(loan_data_strings[:,2] == "", 60, loan_data_strings[:,2])

#Grade and Sub-grade
#Filling the grades (for example if we dont know the subgrade but we know the grade, the best possible filler is the grade and number 5)
for i in np.unique(loan_data_strings[:,3])[1:]:
   loan_data_strings[:,4]=np.where((loan_data_strings[:,4]=='') & (loan_data_strings[:,3] == i), i+"5", loan_data_strings[:,4])
#We still have missing values, so we have to create a new worst case scenario, to be the filler
loan_data_strings[:,4]=np.where(loan_data_strings[:,4] == "", "H1", loan_data_strings[:,4])

#Now the information on grade is also carried in sub grade, therefore the grade column is no longer useful, so we can remove it
#Removing the grade column
loan_data_strings = np.delete(loan_data_strings,3, axis=1)
header_strings = np.delete(header_strings,3)

#Let's convert the sub grade into numeric data for better data analysis
#First we create a dictionary in which the subgrade is asigned into a number. A1=1 and H1=36 (min and max numbers)
keys=list(np.unique(loan_data_strings[:,3]))
values=list(range(1,np.unique(loan_data_strings[:,3]).shape[0]+1))
dict_sub_grade=dict(zip(keys,values))

#Here we convert the sub grades into numbers
for i in np.unique(loan_data_strings[:,3]):
   loan_data_strings[:,3]=np.where(loan_data_strings[:,3] == i, dict_sub_grade[i], loan_data_strings[:,3])

#Verification status
loan_data_strings[:,4]=np.where((loan_data_strings[:,4] == "") | (loan_data_strings[:,4] == "Not Verified"), 0, 1)

#URL
#We notice that we can strip the "https://www.lendingclub.com/browse/loanDetail.action?loan_id=" part of the URL and the id remains
loan_data_strings[:,5] = np.chararray.strip(loan_data_strings[:,5], "https://www.lendingclub.com/browse/loanDetail.action?loan_id=")
#Now we want to check if the remaining id is identical to the id numeric column we have before
loan_data_numeric[:,0].astype(dtype = np.int32)
loan_data_strings[:,5].astype(dtype = np.int32)
print(np.array_equal(loan_data_numeric[:,0].astype(dtype = np.int32), loan_data_strings[:,5].astype(dtype = np.int32)))
#Its TRUE so we can delete the URL column, because the data is already contained in another column
loan_data_strings = np.delete(loan_data_strings, 5, axis = 1)
header_strings = np.delete(header_strings, 5)

#State address

header_strings[5] = "state_address"

#Filling the missing values with 0
loan_data_strings[:,5] = np.where(loan_data_strings[:,5] == "", 0, loan_data_strings[:,5])

#Dividing the states into 4 categories
states_west = np.array(['WA', 'OR','CA','NV','ID','MT', 'WY','UT','CO', 'AZ','NM','HI','AK'])
states_south = np.array(['TX','OK','AR','LA','MS','AL','TN','KY','FL','GA','SC','NC','VA','WV','MD','DE','DC'])
states_midwest = np.array(['ND','SD','NE','KS','MN','IA','MO','WI','IL','IN','MI','OH'])
states_east = np.array(['PA','NY','NJ','CT','MA','VT','NH','ME','RI'])

#We assign that West=1, South=2, Midwest=3, East=4
loan_data_strings[:,5] = np.where(np.isin(loan_data_strings[:,5], states_west), 1, loan_data_strings[:,5])
loan_data_strings[:,5] = np.where(np.isin(loan_data_strings[:,5], states_south), 2, loan_data_strings[:,5])
loan_data_strings[:,5] = np.where(np.isin(loan_data_strings[:,5], states_midwest), 3, loan_data_strings[:,5])
loan_data_strings[:,5] = np.where(np.isin(loan_data_strings[:,5], states_east), 4, loan_data_strings[:,5])

print(np.unique(loan_data_strings[:,5]))

#Our variables look like numbers, but their data type is not. So we have to convert them into numbers so that our numpy functions can work
loan_data_strings = loan_data_strings.astype(dtype = int)
print(loan_data_strings)

#Checkpoint
checkpoint_strings = checkpoint("Checkpoint-Strings", header_strings, loan_data_strings)

#At this stage, we've finished cleaning and pre-processing the string type data. We can now move on to the numeric type data
#Funded amount
#Here we replace the temporary fill with the minimum stats of the temporary stats array, for the funded amount column
loan_data_numeric[:,2] = np.where(loan_data_numeric[:,2] == temporary_fill, 
                                  temporary_stats[0, columns_numeric[2]],
                                  loan_data_numeric[:,2])
loan_data_numeric[:,2]

#The other numerical values need to be replaced with the maximum stats of the temporary stats array. So we do it in a for loop
for i in [1,3,4,5]:
    loan_data_numeric[:,i] = np.where(loan_data_numeric[:,i] == temporary_fill,
                                      temporary_stats[2, columns_numeric[i]],
                                      loan_data_numeric[:,i])

#In order to manipulate the currency change column, we need to find the euro-usd exchange rate.
#First we read the csv file with the exchange rates.
EUR_USD  = np.genfromtxt(open_file_in_same_directory("EUR-USD.csv"), delimiter = ",",skip_header= 1, autostrip= True, usecols=3)
print(EUR_USD)

#We can now add the euro-usd exchange rate to the loan data
exchange_rate = loan_data_strings[:,0]

for i in range(1,13):
    exchange_rate = np.where(exchange_rate == i,
                             EUR_USD[i-1],
                             exchange_rate)    

exchange_rate = np.where(exchange_rate == 0,
                         np.mean(EUR_USD),
                         exchange_rate)

exchange_rate


exchange_rate = np.reshape(exchange_rate, (10000,1))
loan_data_numeric = np.hstack((loan_data_numeric, exchange_rate)) #We now have exchange rate added to the data
#Expanding the header 
header_numeric = np.concatenate((header_numeric, np.array(['exchange_rate'])))

#Now that we have our exchange rates, we notice that 4 columns of the numerical loan data array, are represented win US dollars instead of Euros.
#In order to convert them into dollars all together and not seperately, we create a dollar column of these 4 columns.
columns_dollar = np.array([1,2,4,5])

#Here we calculate the values in euros for these 4 columns
for i in columns_dollar:
    loan_data_numeric = np.hstack((loan_data_numeric, np.reshape(loan_data_numeric[:,i] / loan_data_numeric[:,6], (10000,1))))

#Now we must add additional headers. Specifically, we add the euro columns to our data set
header_additional = np.array([column_name + '_EUR' for column_name in header_numeric[columns_dollar]])
header_numeric = np.concatenate((header_numeric, header_additional))

header_numeric[columns_dollar] = np.array([column_name + '_USD' for column_name in header_numeric[columns_dollar]])
#Rearranging the columns for better readability and understanding of the data set
columns_index_order = [0,1,7,2,8,3,4,9,5,10,6]
header_numeric = header_numeric[columns_index_order]
loan_data_numeric = loan_data_numeric[:,columns_index_order]

#Interest rate
#We have to transform the data so they can fit the 0 to 1 range which is the interest rate
loan_data_numeric[:,5] = loan_data_numeric[:,5]/100

#Checkpoint
checkpoint_numeric = checkpoint("Checkpoint-Numeric", header_numeric, loan_data_numeric)

#Now we can finaly create or final dataset
#After using the shape method, we found out that our numeric and string data set have the same number of rows, which means we can hstack them
loan_data = np.hstack((checkpoint_numeric['data'], checkpoint_strings['data']))
header_full = np.concatenate((checkpoint_numeric['header'], checkpoint_strings['header']))

#We can sort the dataset using the ID column as index.
loan_data = loan_data[np.argsort(loan_data[:,0])]

#Storing the dataset

loan_data = np.vstack((header_full, loan_data))
np.savetxt("loan-data-preprocessed.csv", 
           loan_data, 
           fmt = '%s',
           delimiter = ',')


