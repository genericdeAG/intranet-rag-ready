# web-summarizer

This is a tool that scrapes a sharepoint site and cleans, transform and structures the data into markdown format. 

The purpose of this is to integrate the data into a vector database, facilitating RAG applications.

It is optimized for German language but will probably work for other languages as well.

## Requirements
Python 3.10 is required.

You need to have an OpenAI API key or Azure OpenAI model deployed.

You need to have an Azure tenant ID and client ID.

## Get started

To get started copy copy the ``.env.template``and rename it to ``.env``. Add your OpenAI / Azure OpenAI credentials and default file path if you want.´

### Install the packages (ideally in a venv)

``pip install -r requirements.txt``


## Run tool with CLI commands

``python src/main.py`` (uses default file path from ``.env``)

``python src/main.py data/intranet_homepage.html`` (uses specified html file)

``python src/main.py https://www.my-company.sharepoint.com`` (uses specified url, only works for public sharepoint sites)

### Contact me if you have feedback or feature requests.