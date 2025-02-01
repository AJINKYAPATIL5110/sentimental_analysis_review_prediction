**README.md**
```
# FastAPI Sentiment Analysis API

FastAPI is a modern, high-performance web framework for building APIs with Python. It is designed for speed and ease of use, supporting asynchronous programming and automatic data validation with Pydantic.

This FastAPI application allows an admin user to upload a CSV file containing review text, process it for sentiment analysis, and store the results in `export.csv`.

## Features
- Static login for an admin user
- CSV file upload with `id` and `review_text`
- Sentiment analysis processing
- Processed data saved in `export.csv`
- JWT token authentication for security

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/your-repo.git
cd your-repo
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI Server
```bash
uvicorn main:app --reload
```

## Authentication (Admin Login)
### **How FastAPI Uses JWT and Bearer Token Authentication**
FastAPI uses JWT (JSON Web Token) for authentication, which provides a secure way to manage user sessions. The authentication is handled using a **Bearer Token**, which must be included in API requests.

#### **Steps to Authenticate and Obtain a Token**
1. **Admin logs in with predefined credentials**
```bash
POST http://127.0.0.1:8000/login/
Body: x-www-form-urlencoded
  - username: admin
  - password: admin123
```
2. **FastAPI generates a JWT token, which expires after a defined period.**
3. **The token must be included in the `Authorization` header for future requests:**
```bash
Authorization: Bearer <access_token>
```

## Upload CSV File
```bash
POST http://127.0.0.1:8000/upload_csv/
Headers: 
  Authorization: Bearer <access_token>
Body: 
  file (form-data): Upload your CSV file
```

## Retrieve Processed Data
Once uploaded, the processed data is stored in `export.csv`.
```bash
cat export.csv  # On Windows use `type export.csv`
```

## Full Process to Clone and Use the Repository
### 1. Clone the Repository
```bash
git clone https://github.com/your-repo.git
cd your-repo
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Server
```bash
uvicorn main:app --reload
```

### 5. Authenticate and Obtain a JWT Token
- Send a `POST` request to `/login/` with admin credentials.
- Copy the returned JWT token.
- Include the token in the `Authorization` header for future requests.

### 6. Upload a CSV File
- Send a `POST` request to `/upload_csv/` with a CSV file containing `id` and `review_text`.
- Ensure the request includes the `Authorization: Bearer <access_token>` header.

### 7. Retrieve Processed Data
- The processed data is saved in `export.csv`.
- Open the file to view sentiment analysis results.

## Notes
- Ensure your CSV file has columns `id` and `review_text`.
- The processed file contains `id, review_text, sentiment, confidence_score`.
- Use the JWT token in the `Authorization` header for secure access to endpoints.

Happy coding! 🚀
```