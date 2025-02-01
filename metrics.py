import csv
from datetime import datetime

def log_metrics(user_id, review_text, sentiment, confidence_score, execution_time):
    """Log metrics to a specified CSV file."""
    with open('python_data_analysis/1429_1.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), user_id, review_text, sentiment, confidence_score, execution_time])
