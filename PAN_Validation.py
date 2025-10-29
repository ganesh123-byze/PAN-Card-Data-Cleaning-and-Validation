import pandas as pd
import os 
import re
os.chdir(r"C:\Users\Ganesh\OneDrive\Desktop\Projects\PAN_CARD_Validation")

df = pd.read_csv("dirty_pan_dataset.csv")
print(df.head(10))
print("Total Length of Records :\n",len(df))
Total_records = len(df)

#converting the dataframe object into string type for data cleaning
#remove the spaces from pan_numbers using the strip function
#convert the pan numbers into upper case
df["PAN_Numbers"] = df["PAN_Numbers"].astype('string').str.strip().str.upper()
print(df.head(10))

#Find the empty and NA records in the dataframe
print('\n')
print(df[df['PAN_Numbers'] == ''])
print(df[df['PAN_Numbers'].isna()])
print("Total Empty Pan Records are :\n",len(df[df['PAN_Numbers'].isna()]))

#converting the ''empty columns in pan_numbers to NA values
#also removeing the NA Values
df = df.replace({'PAN_Numbers' : ''},pd.NA).dropna(subset = 'PAN_Numbers')

#here we are complete cleaning in pan column
print("After Removeing the NA Pan values the length is :\n",len(df))

#Now we have to clean the persons (Name) coulumn who don't having the name

print('\n')
#Find the empty and NA Values in Names column
print(df[df['Name'] == ''])
print(df[df['Name'].isna()])

#Get the length of the NA values in names column
print("Length of the Name column contains the NA Values :\n",len(df[df['Name'].isna()]))

#now replace the empty to NA Values and remove them from dataframe
df = df.replace({'Name':''},pd.NA).dropna(subset = 'Name')
print("After removeing the NA values in the names column the length is :\n",len(df))


#Removeing the duplicates in the dataframe 
#Removing the duplicates in pan_numbers
print("Total Records :",len(df))
#find the unique values
print("Unique Values :",df['PAN_Numbers'].nunique())

#Droping the duplicates and keepin the first record only
df = df.drop_duplicates(subset = 'PAN_Numbers', keep = "first")

print("Total Records :",len(df))

#similarly remove the duplicates in name column
print("Unique Values in Name Column :",df["Name"].nunique())
df = df.drop_duplicates(subset = 'Name',keep = "first")
print("Total Records :",len(df))

# *** Data Cleaning is completed ****

#Start the Data Validation

#check the pan Number as adjcent repetation
def has_adjacent_repetation(pan):
   # for i in range(len(pan)-1):
       # if pan[i] == pan[i+1]:
          #  return True
    #return False    
     # OR This function alternative code
    return any(pan[i] == pan[i+1] for i in range(len(pan)-1))  #(List Comprehension)

"""print(has_adjacent_repetation('ABCDE'))
print(has_adjacent_repetation('ZZXYZ'))
print(has_adjacent_repetation('MNOPQ'))
print(has_adjacent_repetation('ABCFF'))"""

#Check The Pan number having the any sequence

def has_sequence(pan):
   #for i in range(len(pan)-1):
        #Here ord function gives the ascii value of the charcter
        #if ord(pan[i+1]) - ord(pan[i]) != 1:
            #return False
    #return True  
      # Or
    return all(ord(pan[i+1]) - ord(pan[i]) == 1 for i in range(len(pan)-1)) #List comprehension

"""print(has_sequence('ABCDE'))
print(has_sequence('CTYMO'))
print(has_sequence('NSBNE'))"""


#Checking the pan Number is valid or not based on the conditions
def is_valid(pan):
    if len(pan) != 10:
        return False
    
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$",pan):
        return False
    
    if has_adjacent_repetation(pan):
        return False
    
    if has_sequence(pan):
        return False
    
    return True

df['Status'] = df['PAN_Numbers'].apply(lambda x : "Valid" if is_valid(x) else "In Valid")
print(df.head(10))

Valid_records = (df['Status'] == 'Valid').sum()
In_Valid_records = (df['Status'] == 'In Valid').sum()
Missing_count = Total_records - (Valid_records + In_Valid_records)

print("Total Records =",Total_records)
print("Valid Reocrds =",Valid_records)
print("In valid records =",In_Valid_records)
print("Missing Records =",Missing_count)

df_summary = pd.DataFrame({"TOTAL PROCESSED RECORDS ":[Total_records]
                          ,"TOTAL VALID COUNT ":[Valid_records]
                          ,"TOTAL IN VALID COUNT ":[In_Valid_records]
                          ,"TOTAL MISSING RECORDS ":[Missing_count]})

print(df_summary.head())


df.to_csv("PAN_VALIDATION_RESULT.csv")
df_summary.to_csv("PAN_VALIDATION_SUMMARY.csv")


import matplotlib.pyplot as plt

counts = df['Status'].value_counts()
plt.pie(counts, labels = counts.index, autopct = '%1.1f%%',startangle = 90)
plt.title("PAN Validation Summary")
plt.show()