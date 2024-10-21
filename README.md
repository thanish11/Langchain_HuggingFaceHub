# Ovarian Cancer Chatbot
![Flask](https://img.shields.io/badge/Flask-v2.2.2-blue)
![Langchain](https://img.shields.io/badge/Langchain-v0.0.100-orange)
![Hugging Face](https://img.shields.io/badge/HuggingFace-v4.22.1-red)
![Embedding Model](https://img.shields.io/badge/Embedding_Model-BAAI%2Fbge--small--en--v1.5-lightgrey)  

## Overview
This chatbot leverages **Mistral 7B** and **LangChain** to provide ovarian cancer-related information and calculate **ROMA scores** based on biomarker inputs. It can also answer general queries and extract relevant data from PDFs.

## Features
- **ROMA Score Calculation**: Risk assessment using CA125 and HE4 biomarkers.
- **PDF Querying**: Retrieve information from stored PDFs on hospitals, diet plans, and ovarian cancer.
- **General Health Chat**: Responds to general queries using HuggingFace models.

##ROMA Score Calculation
- **Postmenopause** 

    ROMA = (exp(-12 + 2.38 * ln(HE4) + 0.0626 * ln(CA125)) / 
        (1 + exp(-12 + 2.38 * ln(HE4) + 0.0626 * ln(CA125)))) * 100 

- **Pre-menopause**

    ROMA = (exp(-8.09 + 1.04 * ln(HE4) + 0.732 * ln(CA125)) / 
        (1 + exp(-8.09 + 1.04 * ln(HE4) + 0.732 * ln(CA125)))) * 100 

## Tech Stack
- **HuggingFace Hub**: Hosts the **Mistral 7B** model.
- **LangChain**: Manages PDFs and FAISS-based vector search.
- **Python & Flask**: Backend for chat handling.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/thanish11/Langchain_HuggingFaceHub.git
   cd Langchain_HuggingFaceHub
