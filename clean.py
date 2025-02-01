import pandas as pd

def clean_csv_with_pandas(input_file: str, output_file: str):
    try:
        # Read the input CSV file into a Pandas DataFrame
        df = pd.read_csv("amazon_reviews.csv")
        
        # Select only the 'id' and 'review_text' columns
        cleaned_df = df[['id', 'review_text']]
        
        # Write the cleaned DataFrame to an output CSV file
        cleaned_df.to_csv(output_file, index=False)
        
        print(f"CSV cleaned and saved as {output_file}")
    
    except Exception as e:
        print(f"Error while processing CSV: {e}")

# Example usage
clean_csv_with_pandas('input.csv', 'cleaned_output.csv')
