import pandas as pd

# Read the original CSV file
input_csv_path = 'D:/chromedriver-win64/add/converted_reviews.csv'
output_csv_path = 'D:/chromedriver-win64/add/negative_converted_reviews.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_path)

# Filter rows with negative sentiment
negative_df = df[df['Sentiment'] == 'negative']

# Save the filtered DataFrame to a new CSV file
negative_df.to_csv(output_csv_path, index=False)

print("Filtered data with negative sentiment has been saved to", output_csv_path)