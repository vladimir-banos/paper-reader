# Paper Reader

A Python tool that automatically summarizes academic papers (PDF) using Google Gemini AI and outputs structured summaries in LaTeX format, ready to use with `\input{}` in Overleaf.

## What it does

- Reads PDF papers from `papers/input/your-folder/`
- Applies a customizable template to structure the summary
- Generates a structured `.tex` file for each paper
- Saves outputs to `papers/output/your-folder/`
- Skips already-processed papers (resumable sessions)
- Processes up to 15 papers per session with automatic pauses

## Templates

Two templates are included:

- **default** — for general economics papers: research question, theoretical framework, empirical strategy, data, findings, mechanisms, assumptions, limitations, contribution, extensions. Prompt written in English.
- **default_es** — same structure, prompt written in Spanish.

You can create your own template by adding a `.txt` file to the `templates/` folder. No special format required — just write plain text instructions describing what you want the summary to include.

## Requirements

- Python 3.8+
- Google Gemini API key (free tier available at [aistudio.google.com](https://aistudio.google.com))

## Setup

1. Clone the repository
   ```
   git clone https://github.com/vladimir-banos/paper-reader.git
   cd paper-reader
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root folder
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Add your PDF papers to `papers/input/your-folder-name/`

## Usage

```
python main.py
```

The tool will ask you to select a template and a folder. Summaries are saved as `.tex` files in `papers/output/`.

## Project structure

```
paper-reader/
├── main.py
├── config.py
├── requirements.txt
├── .env              ← your API key (not tracked by git)
├── .gitignore
├── templates/
│   ├── default.txt
│   └── default_es.txt
└── papers/
    ├── input/        ← place your PDFs here
    └── output/       ← summaries saved here
```

## Author

Vladimir Baños — Economics student, Universidad de Piura (UDEP)

---

*README también disponible en [español](README_es.md)*