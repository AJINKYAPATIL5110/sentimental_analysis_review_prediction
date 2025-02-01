import logging

# Configure logging
logging.basicConfig(
    filename='api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_request(request):
    logging.info(f"Request: {request}")

def log_response(response):
    logging.info(f"Response: {response}")

def log_error(error):
    logging.error(f"Error: {error}")
