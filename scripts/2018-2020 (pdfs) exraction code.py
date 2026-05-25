import pdfplumber
import pandas as pd
import re
import os

def de_double_text(text):
    """Fixes '3300..5588' -> '30.58' doubling issue."""
    if not text: return ""
    cleaned = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i+1]:
            cleaned.append(text[i])
            i += 2
        else:
            cleaned.append(text[i])
            i += 1
    return "".join(cleaned)

def extract_date_from_filename(filename):
    """
    Extracts MM and YYYY from filename (e.g., '12 - 2020').
    Returns 'YYYY-MM' format for easy sorting.
    """
    # Pattern to find 1-2 digits (month) followed by a separator and 4 digits (year)
    match = re.search(r'(\d{1,2})\s*[-_]\s*(\d{4})', filename)
    if match:
        month = match.group(1).zfill(2)
        year = match.group(2)
        return f"{year}-{month}"
    return "Unknown"

def process_all_pdfs(folder_path, output_csv):
    all_rows = []
    unit_keywords = ['k.g', 'gram', 'Liter', 'single', 'pair', 'pieces']
    target_pages = [10, 11, 12]

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    print("Starting extraction process...")
    print("-" * 40)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            file_date = extract_date_from_filename(filename)
            
            print(f"Processing: {filename} | Extracted Date: {file_date}")

            try:
                with pdfplumber.open(file_path) as pdf:
                    for page_num in target_pages:
                        if page_num > len(pdf.pages):
                            continue
                        
                        page = pdf.pages[page_num - 1]
                        text = page.extract_text()
                        if not text:
                            continue
                        
                        lines = text.split('\n')
                        for line in lines:
                            clean_line = de_double_text(line)
                            numbers = re.findall(r'\(?\d+\.?\d*\)?', clean_line)
                            
                            # Row must have at least 5 numeric groups
                            if len(numbers) >= 5:
                                first_num = numbers[0]
                                name_part = clean_line.split(first_num)[0].strip()
                                price_val = numbers[3]
                                
                                unit = "N/A"
                                for kw in unit_keywords:
                                    if kw.lower() in clean_line.lower():
                                        unit = kw
                                        break
                                
                                # Validate that there's a commodity name
                                if name_part and any(c.isalpha() for c in name_part):
                                    all_rows.append({
                                        "Date": file_date,
                                        "Commodity": name_part,
                                        "Price": price_val,
                                        "Unit": unit,
                                        "File_Source": filename
                                    })
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    if all_rows:
        df = pd.DataFrame(all_rows)
        # Filter out repeated headers
        df = df[~df['Commodity'].str.contains("Commodity|Change|Price", case=False)]
        
        # Sort by Date for a clean chronological timeline
        df = df.sort_values(by='Date')
        
        # Save to CSV
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print("-" * 40)
        print(f"Done! Extracted {len(df)} rows in total.")
        print(f"Output saved to: {output_csv}")
    else:
        print("-" * 40)
        print("No valid data found in any of the PDF files.")

# --- Execution ---
folder_name = 'E:\\تالتة جامعة\\second term\\data science\\project\\dataset' 
output_file = 'final_extracted_data.csv'
process_all_pdfs(folder_name, output_file)