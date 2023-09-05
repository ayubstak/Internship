import pandas as pd
import numpy as np

# Read the CSV file
csv_file_path = 'D:/chromedriver-win64/last_merge/dataset2.csv'
df = pd.read_csv(csv_file_path)

# Shuffle the rows
shuffled_df = df.sample(frac=1, random_state=42)  # Setting random_state for reproducibility

# Save the shuffled data to a new CSV file
shuffled_csv_file_path = 'D:/chromedriver-win64/last_merge/shuffled_dataset2.csv'  # Replace with the desired path for the shuffled CSV file
shuffled_df.to_csv(shuffled_csv_file_path, index=False)

print("Shuffling complete. Shuffled CSV file saved.")