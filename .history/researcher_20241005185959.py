# Import necessary libraries
from exa_py import Exa  # For web search functionality
from openai import OpenAI  # For AI-powered text generation
import os  # For interacting with the operating system
import json  # For JSON data handling
from enum import Enum  # For creating enumerated types
import threading  # For parallel processing
from termcolor import colored  # For colored console output
import schedule  # For scheduling recurring tasks
import time  # For time-related operations
from datetime import datetime  # For working with dates and times
import base64  # For encoding the logo image

# Define an enumeration for supported languages
class Language(Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    ITALIAN = "Italian"
    PORTUGUESE = "Portuguese"


# Initialize the Exa client for web searches
def initialize_exa():
    return Exa(os.getenv('EXA_API_KEY'))

# Perform a web research with Exa api
def perform_web_research(exa_client, query, num_results=5):
    result = exa_client.search_and_contents(
        query,
        type="neural",
        use_autoprompt=True,
        num_results=num_results,
        text=True,
        start_published_date="2024-7-16",
    )
    return result

# Convert search results to a serializable format
def serialize_search_results(search_result):
    return {
        "results": [
            {
                "title": item.title,
                "url": item.url,
                "text": item.text,
            } for item in search_result.results
        ],
    }

# Prepare the content for GPT processing
def prepare_content_for_gpt(serialized_results):
    content = "Create a markdown article about the following AI Risk news, using the relevant URLs as citations where necessary:\n\n"
    for item in serialized_results["results"]:
        content += f"Title: {item['title']}\nURL: {item['url']}\nText: {item['text']}\n\n"
    return content

# Generate an article using OpenAI's GPT model
def generate_article(openai_client, content):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert journalist specializing in writing comprehensive and engaging articles about the latest developments in Large Language Models (LLMs), AI and AI risk. Your task is to create a well-structured, informative markdown article based solely on the provided news snippets. Use the given URLs as citations where appropriate to support your writing. Focus on synthesizing the information coherently, highlighting key points, and providing insightful analysis within the context of the LLM field."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Save the generated article to a file
def save_article(article, folder, filename='llm_news_article.md'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    print(colored(f"Markdown article saved to {filepath}", "green"))

# Save the raw search results to a JSON file
def save_raw_results(serialized_results, folder, filename='search_results.json'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(serialized_results, f, indent=4, ensure_ascii=False)
    print(colored(f"Raw search results saved to {filepath}", "yellow"))

# Translate the article to a target language using GPT
def translate_article(openai_client, content, target_language):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a professional translator and journalist. Translate and create a well-structured, informative markdown article in {target_language} based on the provided LLM news snippets. Use the given URLs as citations where appropriate. Focus on synthesizing the information coherently, highlighting key points, and providing insightful analysis within the context of the LLM field."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Save the translated article to a file
def save_translated_article(article, language, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    print(colored(f"{language.capitalize()} article saved to {filepath}", "blue"))

# Generate an HTML version of the article using GPT
def generate_html(openai_client, content, language, logo_path, author_name):
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    html_template = f"""
    <!DOCTYPE html>
    <html lang="{language.lower()[:2]}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Risk: Aligning Technology with Safety and Innovation</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 text-white font-sans">
        <div class="container mx-auto px-4 py-8 max-w-4xl">
            <header class="mb-8">
                <div class="flex items-center justify-between mb-4">
                    <img src="data:image/png;base64,{encoded_string}" alt="Digital Human Assistants Logo" class="h-16">
                    <h1 class="text-3xl font-bold">Digital Human Assistants</h1>
                </div>
                <h2 class="text-4xl font-bold mb-2">AI Risk: Aligning Technology with Safety and Innovation</h2>
                <p class="text-xl text-gray-400">Exploring the Challenges and Opportunities in Contemporary AI Systems</p>
            </header>
            <main>
                <!-- Article content will be inserted here -->
            </main>
            <footer class="mt-8 text-center text-gray-400">
                <p>Author: {author_name}</p>
                <p>&copy; {datetime.now().year} Digital Human Assistants. All rights reserved.</p>
            </footer>
        </div>
    </body>
    </html>
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a web developer and journalist specializing in creating beautiful, modern web pages using Tailwind CSS. Create a well-structured, informative HTML article in {language} based on the provided LLM news snippets. Use the given URLs as citations where appropriate. The page should use dark mode Tailwind styling, be responsive, and visually appealing. Focus on synthesizing the information coherently, highlighting key points, and providing insightful analysis within the context of the LLM field. Insert your content into the provided HTML template, replacing the comment '<!-- Article content will be inserted here -->'. Use appropriate Tailwind classes to style the content similar to the header, with proper spacing, font sizes, and text colors."},
            {"role": "user", "content": f"HTML Template:\n{html_template}\n\nArticle Content:\n{content}"}
        ]
    )
    return response.choices[0].message.content

# Save the generated HTML page to a file
def save_html_page(html_content, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(colored(f"HTML page saved to {filepath}", "magenta"))

# Get user input for target languages
def get_target_languages():
    print(colored("Available languages:", "cyan"))
    for i, lang in enumerate(Language, 1):
        print(colored(f"{i}. {lang.value}", "cyan"))
    
    selected_langs = []
    while True:
        choice = input(colored("Enter the number of the language you want to translate to (or 'done' to finish): ", "cyan"))
        if choice.lower() == 'done':
            break
        try:
            lang_index = int(choice) - 1
            if 0 <= lang_index < len(Language):
                selected_langs.append(Language(list(Language)[lang_index].value))
            else:
                print(colored("Invalid choice. Please try again.", "red"))
        except ValueError:
            print(colored("Invalid input. Please enter a number or 'done'.", "red"))
    
    return selected_langs

# Process a single language (translate, generate HTML, and save files)
def process_language(openai_client, content, lang, folder, logo_path, author_name):
    translated_article = translate_article(openai_client, content, lang.value)
    save_translated_article(translated_article, lang.value, folder, f"llm_news_article_{lang.value.lower()[:2]}.md")
    html_content = generate_html(openai_client, translated_article, lang.value, logo_path, author_name)
    save_html_page(html_content, folder, f"llm_news_article_{lang.value.lower()[:2]}.html")

# Main task execution function
def run_task(exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = f"llm_news_{timestamp}"
    
    # Perform web search and prepare content
    search_result = perform_web_research(exa_client, query, num_results)
    serialized_results = serialize_search_results(search_result)
    content = prepare_content_for_gpt(serialized_results)

    # Save raw search results
    save_raw_results(serialized_results, folder)

    # Process English version
    english_client = OpenAI(api_key=openai_api_key)
    process_language(english_client, content, Language.ENGLISH, folder, logo_path, author_name)

    # Process other languages in parallel
    threads = []
    for lang in target_languages:
        if lang != Language.ENGLISH:
            thread = threading.Thread(target=process_language, args=(OpenAI(api_key=openai_api_key), content, lang, folder, logo_path, author_name))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(colored(f"Newsletter generation completed. Files saved in folder: {folder}", "green"))

# Function to handle scheduling and execution
def schedule_and_run(schedule_choice, interval, exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name):
    # Run the task immediately
    run_task(exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)
    
    if schedule_choice == 'custom':
        schedule.every(interval).hours.do(run_task, exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)
        print(colored(f"Task scheduled to run every {interval} hours. Press Ctrl+C to stop.", "green"))
    elif schedule_choice == 'weekly':
        schedule.every(7).days.do(run_task, exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)
        print(colored("Task scheduled to run weekly. Press Ctrl+C to stop.", "green"))
    
    # Enter the scheduling loop for future runs
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main function to handle user input and program flow
def main():
    exa_client = initialize_exa()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    logo_path = "C:\\Users\\User\\OneDrive\\Documents\\GitHub\\web-researcher-with scheduler\\Digital Human Assistant Black.png"
    author_name = "Christopher Foster-McBride"

    # Get user input for search query and number of results
    query = input(colored("Enter your web research query: ", "cyan"))
    num_results = int(input(colored("Enter the number of results you want: ", "cyan")))
    
    # Ask if user wants to translate the article
    translate_choice = input(colored("Do you want to translate the article? (yes/no): ", "cyan")).lower()
    target_languages = []
    if translate_choice == 'yes':
        target_languages = get_target_languages()

    # Ask if user wants to schedule recurring execution
    schedule_choice = input(colored("Do you want to schedule recurring execution? (one-time/custom/weekly): ", "cyan")).lower()
    
    if schedule_choice == 'custom':
        interval = int(input(colored("Enter the interval for recurring execution (in hours): ", "cyan")))
        schedule_and_run(schedule_choice, interval, exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)
    elif schedule_choice == 'weekly':
        schedule_and_run(schedule_choice, 168, exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)
    else:
        # Run the task once immediately
        run_task(exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name)

# Entry point of the script
if __name__ == "__main__":
    main()