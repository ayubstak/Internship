import pandas as pd

# Read the CSV file
csv_file_path = 'D:/chromedriver-win64/predicted_analyzed2/predicted_wyeth_nutrition_reviews.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Assuming you have a DataFrame named 'df' with columns 'index', 'Review', and 'Sentiment'
data = {'index': df['index'], 'Review': df['Review'], 'Sentiment': df['Sentiment'], 'product': 'wyeth_nutrition'}
new_df = pd.DataFrame(data)

# Specify the path where you want to save the CSV file
output_path = 'D:/chromedriver-win64/predicted_analyzed2/mentioned_predicted_wyeth_nutrition_reviews.csv'

# Write the DataFrame to a CSV file
new_df.to_csv(output_path, index=False)

print(f'CSV file saved to {output_path}')