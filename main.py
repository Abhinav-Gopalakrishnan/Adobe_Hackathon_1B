import os
import json
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load MiniLM model from offline directory
model = SentenceTransformer('models/minilm-local')

# Directories
pdf_folder = "/content/Collection 1/PDFs/"
input_json_path = "/content/Collection 1/challenge1b_input.json"
output_json_path = "/content/Collection 1/challenge1b_output.json"

def extract_sections(pdf_path):
    sections = []
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                text = " ".join([span["text"] for line in block["lines"] for span in line["spans"]])
                text = text.strip()
                if len(text.split()) >= 5:
                    sections.append({
                        "page_number": page_num + 1,
                        "text": text
                    })
    doc.close()
    return sections

def rank_sections_globally(all_sections, job_description):
    ranked = []
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    for section in all_sections:
        section_embedding = model.encode(section["text"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(job_embedding, section_embedding).item()
        ranked.append({
            "filename": section["filename"],
            "page_number": section["page_number"],
            "text": section["text"],
            "importance_rank": similarity
        })

    ranked.sort(key=lambda x: x["importance_rank"], reverse=True)
    return ranked

def refine_text(text):
    # Basic cleanup; you can improve further
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return ' '.join(lines[:5])

def main():
    # Load input JSON
    with open(input_json_path, 'r') as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    job_description = input_data["job_to_be_done"]["task"]

    all_sections = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            full_path = os.path.join(pdf_folder, filename)
            try:
                sections = extract_sections(full_path)
                for section in sections:
                    section["filename"] = filename
                all_sections.extend(sections)
            except Exception as e:
                logging.warning(f"Error reading {filename}: {e}")

    logging.info(f"Total sections collected: {len(all_sections)}")

    ranked_sections = rank_sections_globally(all_sections, f"{persona}: {job_description}")

    # Format output
    output = {
        "metadata": {
            "persona": persona,
            "job_to_be_done": job_description
        },
        "extracted_sections": []
    }

    for idx, sec in enumerate(ranked_sections):
        output["extracted_sections"].append({
            "document": sec["filename"],
            "page_number": sec["page_number"],
            "section_title": sec["text"][:60] + "...",
            "refined_text": refine_text(sec["text"]),
            "importance_rank": round(sec["importance_rank"], 4)
        })

    with open(output_json_path, "w") as f:
        json.dump(output, f, indent=4)

    print(f"✅ Output saved to {output_json_path}")

if __name__ == "__main__":
    main()
