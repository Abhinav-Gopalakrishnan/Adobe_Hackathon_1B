# Adobe_Hackathon_1B

# Team - Ritzy

## Overview

This project aims to extract meaningful sections from a collection of PDF documents and rank them according to their relevance to a given job description. The extracted sections are then refined and saved into a JSON file, making it easy to review and analyze the most relevant parts of the documents.

## Methodology

The approach relies on Natural Language Processing (NLP) techniques, particularly leveraging a pre-trained sentence transformer model (`SentenceTransformer`) for semantic similarity matching. Here’s a breakdown of the steps involved:

### 1. **PDF Document Parsing**
   The first step in the process is to extract text from PDF files. The tool uses the `fitz` (PyMuPDF) library to open each PDF file and parse its content. The text extraction method retrieves blocks of text from each page and ensures that only blocks with sufficient content (minimum 5 words) are considered. This helps in filtering out irrelevant or noise sections such as headers, footers, or very short fragments.

### 2. **Text Preprocessing**
   Once the text is extracted from each PDF, a preprocessing step is applied. This includes:
   - **Trimming unnecessary whitespace**: Any leading or trailing spaces are removed.
   - **Combining text blocks**: Lines within a block are merged into a single string for ease of processing.

   In this stage, the goal is to ensure the extracted text is clean and structured in a way that makes it easier to rank for relevance.

### 3. **Ranking Sections by Relevance**
   After extracting the sections, each section is ranked based on its relevance to a provided job description. The process works as follows:
   
   - **Job Description Embedding**: The job description (from the input JSON file) is encoded into a dense vector representation using a pre-trained `SentenceTransformer` model (`minilm-local`). This model is designed to understand the semantic meaning of the job description.
   
   - **Section Embedding**: Each extracted text section from the PDF is also encoded into a vector using the same transformer model. These vectors capture the semantic meaning of the sections.
   
   - **Similarity Calculation**: The cosine similarity between the job description vector and each section vector is computed. Cosine similarity measures the angle between two vectors, where a higher similarity score indicates greater relevance.

   - **Ranking**: Based on the cosine similarity scores, the sections are ranked in descending order. The most relevant sections will have higher similarity scores and appear at the top of the list.

### 4. **Refinement of Extracted Sections**
   For readability and conciseness, the top sections are refined:
   - **Trimming to First Few Lines**: Only the first few lines of the text are kept (up to a defined limit of 5 lines). This ensures the text remains short and to the point.
   - **Title Extraction**: A short title (up to 60 characters) is extracted from the section text to provide a preview of its content.

### 5. **Output Generation**
   The final output is stored in a JSON format, which includes:
   - Metadata about the persona (role) and the job description.
   - A list of extracted sections from the PDFs, along with their importance ranking, title, and refined text.

   This JSON file serves as the final deliverable, which can be reviewed and analyzed to identify the most relevant sections for a particular job description.

## Tools & Libraries Used
- `fitz` (PyMuPDF) for PDF text extraction
- `sentence_transformers` for semantic text embeddings and similarity calculation
- `json` for reading and writing structured data

## Conclusion
This methodology effectively combines document parsing, text embedding, and similarity-based ranking to identify and extract the most relevant sections from large sets of PDFs. By refining and ranking the sections based on relevance to a specific job description, it streamlines the process of information retrieval, making it easier to focus on the most pertinent content.
