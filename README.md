# Christianity News Research Tool

This Python script is a versatile tool for conducting web research on Christian news, generating articles, and translating content into multiple languages.

## Key Features

1. Web Search: Utilizes the Exa API to perform web research
2. Article Generation: Uses OpenAI's GPT model to create well-structured markdown articles based on search results.
3. Multi-language Support: Translates articles into various languages (e.g., Spanish, French, German).
4. HTML Generation: Creates visually appealing HTML versions of articles using Tailwind CSS.
5. Scheduling: Offers the option to schedule recurring research tasks.

## How It Works

1. The user inputs a search query and specifies the number of results desired.
2. The script performs a web search using the Exa API.
3. Search results are processed and fed into OpenAI's GPT model to generate an article.
4. The user can choose to translate the article into multiple languages.
5. Both markdown and HTML versions of the articles are saved.
6. Raw search results are also saved for reference.

## Running the Script

1. Ensure all required libraries are installed (see `requirements.txt`).
2. Set up environment variables for API keys (EXA_API_KEY and OPENAI_API_KEY).
3. Run the script: `python research.py`
4. Follow the prompts to input your search query, choose languages, and set up scheduling if desired.

This tool streamlines the process of researching and creating content about the latest developments in Christianity, making it valuable for journalists, researchers, and enthusiasts in the field.
