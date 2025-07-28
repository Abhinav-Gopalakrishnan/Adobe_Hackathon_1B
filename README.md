# Sentence-Transformers Model: all-MiniLM-L6-v2

This repository contains the code for using the all-MiniLM-L6-v2 sentence transformer model from the sentence-transformers library. This model is designed for efficient and high-quality sentence embeddings, which can be used in various NLP tasks like semantic textual similarity, clustering, and more.

## Installation

To run the code in this repository, ensure that you have the necessary libraries installed.

### Requirements:
- Python 3.6 or higher
- sentence-transformers library
- torch library (for PyTorch support)

You can install these dependencies using pip:

bash
pip install sentence-transformers torch


## Usage

### Loading and Saving the Model

The model can be loaded directly from the sentence-transformers library, or you can load the locally saved version after running the following code:

python
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Save the model locally for future use
model.save('models/minilm-local')


Build the Docker Image:
Navigate to the folder containing your Dockerfile and run the following command:

bash
```
docker build -t pdf-processing .
```
This will create a Docker image tagged as pdf-processing.

Run the Docker Container:

Assuming that your project files are in the /path/to/local/folder on your local machine (which contains PDFs/, main.py, challenge1b_input.json, etc.), you can mount the folder as a volume to the container and run the script:

bash
```
docker run -v /path/to/local/folder:/app pdf-processing
```
This will mount your local project folder to the container’s /app folder, allowing the container to access the files and output the result in the same folder.
