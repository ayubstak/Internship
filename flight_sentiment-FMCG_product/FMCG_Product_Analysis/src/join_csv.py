import pandas as pd
import glob

# List all the CSV files in a directory
csv_files = glob.glob('D:/chromedriver-win64/mentioned/*.csv')

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate through each CSV file and merge its data into the merged_data DataFrame
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    merged_data = pd.concat([merged_data, df], ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv('D:/chromedriver-win64/mentioned/merged_mentioned_predicted_analyzed2.csv', index=False)