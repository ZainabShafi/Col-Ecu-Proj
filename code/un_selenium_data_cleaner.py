import pandas as pd
import glob # <--------------- This is built into python.
import numpy as np



# THE BELOW COMBINES THE DATA INTO A SINGLE FILE





# Path to your CSV files
path = 'un_selenium_rip_files/*.csv'  # Adjust this path

# Read all CSV files and concatenate into a single DataFrame
all_files = glob.glob(path)
df_list = [pd.read_csv(file) for file in all_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Sort the combined DataFrame by the TimePeriod column
sorted_df = combined_df.sort_values(by='TimePeriod', ascending=True)

sorted_df = sorted_df.dropna(how='all')

# Optionally, save the sorted DataFrame to a new CSV file
sorted_df.to_csv('formated_csv_files/sorted_combined.csv', index=False)






# # THE BELOW CLEANS/FORMATS THE DATA

# # print(sorted_df['GeoAreaCode'].dtype)

# # print(sorted_df)

# # sorted_df = sorted_df.dropna(how='all')

# #print(sorted_df)

# # area_code_df = sorted_df[sorted_df['GeoAreaCode'].str.contains('2')]

# # print(area_code_df)

# geo_areacode_fix_df = sorted_df[sorted_df['Indicator'] == '17.18.3']

# # print(geo_areacode_fix_df)

# geo_areacode_fix_df.to_csv('formated_csv_files/geo_areacode_fix_df.csv')

# geo_areacode_fix_df_2 = geo_areacode_fix_df.copy()

# geo_areacode_fix_df_2['GeoAreaCode'] = np.nan

# geo_areacode_fix_df_2.to_csv('formated_csv_files/geo_areacode_fix_df_2.csv')

# filtered_df.to_csv('formated_csv_files/filtered_df.csv')

# areacode_format_df.to_csv('formated_csv_files/formated_combined.csv')