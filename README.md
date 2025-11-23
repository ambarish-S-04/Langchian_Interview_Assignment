# Story Character Information Extractor

A Python application that extracts structured character information from story files using LangChain, MistralAI, and ChromaDB.

## Features

- Extract embeddings from story text files
- Store and retrieve character information using a vector database
- Query character information using natural language
- Command-line interface for easy interaction

## Prerequisites

- Python 3.8+
- MistralAI API key
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root with your MistralAI API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```

## Project Structure

```
project/
├── data/
│   └── stories/          # Place your .txt story files here
├── src/
│   ├── embeddings.py     # Embedding computation logic
│   ├── query.py          # Character information retrieval
│   └── utils.py          # Utility functions
├── vectorstore/          # Chroma DB storage (created automatically)
├── .env                  # Environment variables
├── cli.py                # Command-line interface
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Adding Story Files

1. Place your story text files in the `data/stories/` directory.
2. Each file should be a `.txt` file.
3. The filename (without extension) will be used as the `storyTitle`.

## Usage

### 1. Compute Embeddings

Before querying, you need to compute embeddings for your story files:

```bash
python cli.py compute-embeddings
```

This will:
- Load all `.txt` files from `data/stories/`
- Split them into chunks
- Generate embeddings using MistralAI
- Store them in the local Chroma DB at `vectorstore/`

### 2. Get Character Information

To get information about a character:

```bash
python cli.py get-character-info "Character Name"
```

Example:
```bash
python cli.py get-character-info "Sherlock Holmes"
```

This will return structured information about the character in JSON format, including:
- Character name
- Story title
- Character summary
- Relationships with other characters
- Character type (protagonist, villain, side character)

## Example Output

```json
{
  "name": "Sherlock Holmes",
  "storyTitle": "A Study in Scarlet",
  "summary": "Sherlock Holmes is a brilliant consulting detective known for his keen observation skills and deductive reasoning. He solves complex cases that baffle the police.",
  "relations": [
    {"name": "Dr. John Watson", "relation": "Friend and colleague"},
    {"name": "Professor Moriarty", "relation": "Arch-nemesis"},
    {"name": "Mrs. Hudson", "relation": "Landlady"}
  ],
  "characterType": "protagonist"
}
```

## Error Handling

- If a character is not found, the system will return: `{"error": "Character not found"}`
- If the vector store doesn't exist, run `compute-embeddings` first
- If you get API errors, check your `MISTRAL_API_KEY` in the `.env` file

## Troubleshooting

1. **No story files found**
   - Ensure you've placed `.txt` files in the `data/stories/` directory
   - Check file permissions

2. **API Key Issues**
   - Verify your MistralAI API key is correct
   - Ensure the `.env` file is in the project root
   - Make sure the environment variables are loaded (restart your terminal/IDE if needed)

3. **Vector Store Issues**
   - If you get errors about missing vector store, run `compute-embeddings` first
   - Delete the `vectorstore/` directory and recompute embeddings if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://python.langchain.com/) for the LLM framework
- [MistralAI](https://mistral.ai/) for the language model and embeddings
- [Chroma](https://www.trychroma.com/) for the vector database