# web-summarizer

This is a tool that scrapes a sharepoint site and cleans, transform and structures the data into markdown format. 

The purpose of this is to integrate the data into a vector database, facilitating RAG applications.

It is optimized for German language but will probably work for other languages as well.

## Requirements
Python 3.10 is required.

You need to have an OpenAI API key or Azure OpenAI model deployed.

You need to have an Azure tenant ID and client ID (for the Graph API), unless you only use the mock client.

## Get started

To get started copy copy the ``.env.template``and rename it to ``.env``. Add your OpenAI / Azure OpenAI credentials and default file path if you want.´

### Install the packages (ideally in a venv)

``pip install -r requirements.txt``

## Run tool with CLI commands

The tool supports two main commands: `sharepoint` for processing SharePoint sites and `chunk` for chunking the processed markdown files. If chunking is handled by another tool, you can skip the chunking step.

### SharePoint Processing

```bash
# Use default site ID from .env
python src/main.py sharepoint

# Use specific site ID
python src/main.py sharepoint --site-id <site-id>

# Use site ID from environment variables (SITE_ID_1, SITE_ID_2, etc.)
python src/main.py sharepoint --site-id 1

# Use local mock client for testing
python src/main.py sharepoint --mock
```

### Markdown Chunking

```bash
# Process markdown files using default directory (data/extracts)
python src/main.py chunk

# Process markdown files from specific directory
python src/main.py chunk --input-dir path/to/directory
```

## Mocking the Graph API (data)
Get data from Graph Explorer (Sharepoint API) and put json files in data/ms-graph/

### Folder 1: list-all-pages
- File names: identical to site ID

### Folder 2: list-all-webparts

- Subfolder names: identical to respective site ID
- File names: identical to SitePage ID

### site-ids
Add all site IDs from the data your parsed to .env file


----------------------------------------------------------------

#### Contact me if you have feedback or feature requests: joshua.heller@generic.de
