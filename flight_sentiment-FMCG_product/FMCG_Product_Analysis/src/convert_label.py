import pandas as pd

# Read the CSV file
csv_file_path = 'D:/chromedriver-win64/add/reviews.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Map labels from 1 and 0 to "positive" and "negative"
df['label'] = df['label'].map({1: 'positive', 0: 'negative'})

# Save the updated data to a new CSV file
new_csv_file_path = 'D:/chromedriver-win64/add/converted_reviews.csv'  # Replace with the desired path for the new CSV file
df.to_csv(new_csv_file_path, index=False)

print("Conversion complete. New CSV file saved.")