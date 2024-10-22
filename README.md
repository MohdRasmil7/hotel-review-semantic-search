# Technical Document for Semantic Search System

## 1. Introduction

This document outlines the development and deployment of a semantic search system using spaCy, a powerful NLP toolkit. The system allows users to perform semantic searches, retrieving relevant results based on the meaning of queries rather than exact keyword matches.

## 2. Approach

### 2.1. Tool and Libraries

- **Language Model**: spaCy (e.g., `en_core_web_md` for word vectors)
- **Framework**: Flask for web hosting
- **Database**: (if applicable, mention any database used)

### 2.2. Implementation Steps

1. **Data Preparation**: 
   - Collected and preprocessed the dataset to ensure consistency and quality.
   - Used spaCy for tokenization, lemmatization, and vectorization of text data.

2. **Semantic Search Logic**: 
   - Implemented a function to compute cosine similarity between the user's query and the indexed documents.
   - Retrieved the top N most relevant results based on similarity scores.

3. **Web Interface**: 
   - Developed a simple web interface using Flask, allowing users to input queries and view results.

## 3. Hosting

### 3.1. Hosting Platform

The application is hosted on [Azure/Tiiny.host] (choose one based on your assignment). 

### 3.2. Deployment Steps

1. **Environment Setup**: 
   - Created a virtual environment and installed required libraries using `pip install -r requirements.txt`.

2. **Application Configuration**: 
   - Configured the application to run on the specified port.

3. **Deployment**: 
   - Deployed the application on [Azure/Tiiny.host], following the platform's guidelines for deployment.

4. **Access Link**: 
   - The application can be accessed at: [your hosted link].

## 4. Challenges Faced

- **Model Selection**: Choosing the appropriate spaCy model for semantic similarity that balances performance and accuracy.
- **Data Quality**: Ensuring the dataset was clean and well-structured, which required extensive preprocessing.
- **Hosting Issues**: Encountered challenges with environment configuration on [Azure/Tiiny.host], particularly with dependency management and server setup.

## 5. Conclusion

The semantic search system successfully retrieves relevant information based on semantic understanding. This project demonstrates the capabilities of spaCy and the effectiveness of NLP techniques in enhancing search functionalities.

---

### 6. Submission Checklist

- **Code**: [https://github.com/MohdRasmil7/hotel-review-semantic-search]
- **Hosted Link**: [hotel-review-semantic-search-dcafc6c2fgcwd3c8.canadacentral-01.azurewebsites.net]
- **Demo Video**: [Link to the demo video]

