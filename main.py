from google import genai
import pymupdf
import os
import time
from config import GEMINI_API_KEY, MODEL, INPUT_FOLDER, OUTPUT_FOLDER
 
# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
 
# Session limits to avoid API rate errors
SESSION_LIMIT = 15
PAUSE_BETWEEN_PAPERS = 35  # seconds
 
 
def read_pdf(path):
    """Extract full text from a PDF file."""
    doc = pymupdf.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
 
 
def read_template(path):
    """Load a summary template from a .txt file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
 
def already_processed(tex_path):
    """Check if a paper has already been summarized in a previous session."""
    return os.path.exists(tex_path)
 
 
def summarize_paper(pdf_path, tex_path, template):
    """
    Send a paper to Gemini and save the structured LaTeX summary.
    Truncates input to 80,000 characters to stay within token limits.
    """
    name = os.path.basename(pdf_path).replace(".pdf", "")
    print(f"\nProcessing: {name}")
 
    text = read_pdf(pdf_path)
    prompt = f"{template}\n\n--- PAPER ---\n{text[:80000]}"
 
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
 
    os.makedirs(os.path.dirname(tex_path), exist_ok=True)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(f"% {name}\n")
        f.write(f"% Auto-generated summary\n\n")
        f.write(f"\\section*{{{name}}}\n\n")
        f.write(response.text)
 
    print(f"Saved: {tex_path}")
 
 
def select_template():
    """Prompt the user to choose a summary template from the templates/ folder."""
    templates = [f for f in os.listdir("templates") if f.endswith(".txt")]
 
    if not templates:
        print("No templates found in templates/")
        return None, None
 
    print("\nAvailable templates:")
    for i, t in enumerate(templates):
        print(f"  {i+1}. {t.replace('.txt', '')}")
 
    while True:
        choice = input("\nSelect a template (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(templates):
            selected = templates[int(choice) - 1]
            return selected, read_template(os.path.join("templates", selected))
        print("Invalid option. Try again.")
 
 
def select_folder():
    """Prompt the user to choose a subfolder inside papers/input/."""
    subfolders = [
        f for f in os.listdir(INPUT_FOLDER)
        if os.path.isdir(os.path.join(INPUT_FOLDER, f))
    ]
 
    if not subfolders:
        print("No subfolders found in papers/input/")
        return None
 
    print("\nAvailable folders in input:")
    for i, folder in enumerate(subfolders):
        print(f"  {i+1}. {folder}")
 
    while True:
        choice = input("\nSelect a folder (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(subfolders):
            return subfolders[int(choice) - 1]
        print("Invalid option. Try again.")
 
 
def main():
    template_name, template = select_template()
    if not template:
        return
 
    folder = select_folder()
    if not folder:
        return
 
    input_folder = os.path.join(INPUT_FOLDER, folder)
    output_folder = os.path.join(OUTPUT_FOLDER, folder)
 
    all_papers = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
 
    if not all_papers:
        print(f"No PDF files found in {input_folder}")
        return
 
    # Skip papers already processed in previous sessions
    pending = [
        f for f in all_papers
        if not already_processed(os.path.join(output_folder, f.replace(".pdf", ".tex")))
    ]
 
    print(f"\nTemplate:           {template_name.replace('.txt', '')}")
    print(f"Selected folder:    {folder}")
    print(f"Total PDFs:         {len(all_papers)}")
    print(f"Already processed:  {len(all_papers) - len(pending)}")
    print(f"Pending:            {len(pending)}")
 
    if not pending:
        print("\nAll papers in this folder have already been processed.")
        return
 
    # Process up to SESSION_LIMIT papers per run
    batch = pending[:SESSION_LIMIT]
    remaining = pending[SESSION_LIMIT:]
 
    print(f"\nProcessing in this session: {len(batch)}")
    if remaining:
        print(f"Remaining for next session: {len(remaining)}")
    print("\nPapers in this batch:")
    for i, pdf in enumerate(batch):
        print(f"  {i+1}. {pdf}")
 
    print("\nStarting in 3 seconds...")
    time.sleep(3)
 
    for i, pdf in enumerate(batch):
        pdf_path = os.path.join(input_folder, pdf)
        tex_path = os.path.join(output_folder, pdf.replace(".pdf", ".tex"))
        try:
            summarize_paper(pdf_path, tex_path, template)
        except Exception as e:
            print(f"Error processing {pdf}: {e}")
            print("Skipping to next paper...")
 
        if i < len(batch) - 1:
            print(f"Waiting {PAUSE_BETWEEN_PAPERS}s before next paper...")
            time.sleep(PAUSE_BETWEEN_PAPERS)
 
    print(f"\nSession complete. Processed: {len(batch)} papers.")
    if remaining:
        print(f"Note: {len(remaining)} papers still pending. Run again to continue.")
 
 
if __name__ == "__main__":
    main()