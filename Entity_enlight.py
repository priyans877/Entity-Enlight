import streamlit as st
import requests
from bs4 import BeautifulSoup
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import PyPDF2
import docx
import pandas as pd

# Azure Text Analytics credentials (replace with your credentials)
endpoint = "https://aimultiser979867857.cognitiveservices.azure.com/"
key = "af41c07c58894d25882d885b0954cf43"

# Function to authenticate the client
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

# Function to extract text from a web link using BeautifulSoup
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# Function to extract text from uploaded files (PDF, DOCX, TXT)
def extract_text_from_file(file):
    file_type = file.type
    
    if file_type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text
    
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    
    elif file_type == "text/plain":
        return file.read().decode('utf-8')
    
    else:
        st.error("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
        return None

# Function to split text into smaller chunks
def split_text(text, max_size=5120):
    return [text[i:i+max_size] for i in range(0, len(text), max_size)]

# Function to analyze text using Azure Text Analytics
def analyze_text_with_azure(text_chunks):
    client = authenticate_client()
    sentiments = []
    
    for chunk in text_chunks:
        try:
            documents = [chunk]
            response = client.analyze_sentiment(documents=documents)[0]
            sentiments.append(response)
        except Exception as e:
            st.error(f"Error analyzing text with Azure: {e}")
            return None
    
    return sentiments

# Function to aggregate sentiment results
def aggregate_sentiment_results(sentiments):
    total_positive = total_neutral = total_negative = 0
    for sentiment in sentiments:
        total_positive += sentiment.confidence_scores.positive
        total_neutral += sentiment.confidence_scores.neutral
        total_negative += sentiment.confidence_scores.negative

    count = len(sentiments)
    return {
        "positive": total_positive / count,
        "neutral": total_neutral / count,
        "negative": total_negative / count,
    }

# Function to extract entities using Azure Text Analytics
def extract_entities_with_azure(text_chunks):
    client = authenticate_client()
    entities = []
    
    for chunk in text_chunks:
        try:
            documents = [chunk]
            response = client.recognize_entities(documents=documents)[0]
            entities.append(response.entities)
        except Exception as e:
            st.error(f"Error extracting entities with Azure: {e}")
            return None
    
    return entities

# Function to categorize and display entities
def categorize_entities(entities):
    categorized_entities = {
        "Person": [],
        "Location": [],
        "Organization": [],
        "Date":[],
        "Time":[],
        "Quantity":[],
        "Other": []
    }
    
    for entity_list in entities:
        for entity in entity_list:
            if entity.category == "Person":
                categorized_entities["Person"].append(entity.text)
            elif entity.category == "Location":
                categorized_entities["Location"].append(entity.text)
            elif entity.category == "Organization":
                categorized_entities["Organization"].append(entity.text)
            elif entity.category == "Date":
                categorized_entities["Date"].append(entity.text)
            elif entity.category == "Time":
                categorized_entities["Time"].append(entity.text)
            elif entity.category == "Quantity":
                categorized_entities["Quantity"].append(entity.text)
            else:
                categorized_entities["Other"].append(entity.text)
    
    # Convert to a DataFrame for better visualization
    entity_data = pd.DataFrame({
        "Person": pd.Series(categorized_entities["Person"]).dropna(),
        "Location": pd.Series(categorized_entities["Location"]).dropna(),
        "Organization": pd.Series(categorized_entities["Organization"]).dropna(),
        "Date": pd.Series(categorized_entities["Date"]).dropna(),
        "Time": pd.Series(categorized_entities["Time"]).dropna(),
        "Quantity": pd.Series(categorized_entities["Quantity"]).dropna(),
        "Other": pd.Series(categorized_entities["Other"]).dropna(),
    })
    
    return entity_data

# Streamlit UI
st.title("EntityEnlight: Unveiling Insights through Extraction")

# Option selection
option = st.selectbox("Choose the input method:", ("None", "Webpage URL", "Upload File", "Enter Text"))

# Webpage URL input
if option == "Webpage URL":
    url = st.text_input("Enter the URL of the webpage to extract text:")
    
    if url:
        st.write(f"Extracting text from: {url}")
        web_text = extract_text_from_url(url)
        
        if web_text:
            st.subheader("Extracted Text from Webpage")
            st.text_area("Text from Webpage:", web_text, height=300)
            
            text_chunks = split_text(web_text)
            
            if st.button("Analyze Webpage Text with Azure"):
                sentiments = analyze_text_with_azure(text_chunks)
                
                if sentiments:
                    aggregated_results = aggregate_sentiment_results(sentiments)
                    st.subheader("Aggregated Sentiment Analysis (Webpage)")
                    st.write(f"Overall Sentiment: Positive: {aggregated_results['positive']:.2f}, "
                             f"Neutral: {aggregated_results['neutral']:.2f}, "
                             f"Negative: {aggregated_results['negative']:.2f}")
                
                entities = extract_entities_with_azure(text_chunks)
                if entities:
                    st.subheader("Extracted Entities (Webpage)")
                    entity_data = categorize_entities(entities)
                    st.table(entity_data)

# File Upload section
elif option == "Upload File":
    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT):")

    if uploaded_file:
        file_text = extract_text_from_file(uploaded_file)
        
        if file_text:
            st.subheader("Extracted Text from File")
            st.text_area("Text from File:", file_text, height=300)
            
            file_text_chunks = split_text(file_text)
            
            if st.button("Analyze File Text with Azure"):
                file_sentiments = analyze_text_with_azure(file_text_chunks)
                
                if file_sentiments:
                    aggregated_file_results = aggregate_sentiment_results(file_sentiments)
                    st.subheader("Aggregated Sentiment Analysis (File)")
                    st.write(f"Overall Sentiment: Positive: {aggregated_file_results['positive']:.2f}, "
                             f"Neutral: {aggregated_file_results['neutral']:.2f}, "
                             f"Negative: {aggregated_file_results['negative']:.2f}")
                
                file_entities = extract_entities_with_azure(file_text_chunks)
                if file_entities:
                    st.subheader("Extracted Entities (File)")
                    entity_data = categorize_entities(file_entities)
                    st.table(entity_data)

# Text Input section for user input
elif option == "Enter Text":
    user_text = st.text_area("Enter or paste text for analysis:")
    
    if user_text:
        user_text_chunks = split_text(user_text)
        
        if st.button("Analyze User Text with Azure"):
            user_sentiments = analyze_text_with_azure(user_text_chunks)
            
            if user_sentiments:
                aggregated_user_results = aggregate_sentiment_results(user_sentiments)
                st.subheader("Aggregated Sentiment Analysis (User Input)")
                st.write(f"Overall Sentiment: Positive: {aggregated_user_results['positive']:.2f}, "
                         f"Neutral: {aggregated_user_results['neutral']:.2f}, "
                         f"Negative: {aggregated_user_results['negative']:.2f}")
            
            user_entities = extract_entities_with_azure(user_text_chunks)
            if user_entities:
                st.subheader("Extracted Entities (User Input)")
                entity_data = categorize_entities(user_entities)
                st.table(entity_data)
