# Import necessary libraries
from exa_py import Exa  # For web search functionality
from openai import OpenAI  # For AI-powered text generation
import os  # For interacting with the operating system
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file (for local development)
load_dotenv()
import json  # For JSON data handling
from enum import Enum  # For creating enumerated types
import threading  # For parallel processing
from termcolor import colored  # For colored console output
import schedule  # For scheduling recurring tasks
import time  # For time-related operations
from datetime import datetime  # For working with dates and times
import base64  # For encoding the logo image
import re  # For regular expressions

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
    content = "Create a markdown article about world Christianity news from the last 14 days, focusing on mainstream Christianity and do not talk about other religions. Use relevant URLs as citations where necessary. All stories should come from different URLs and publications so we get a wide range of sources and stories from accross the world. from reputable news outlets and Chrisitian news providers. You audeince are Chrisitians, so always start with positive and uplifting Chrisitian stories first.\n\n"
    for item in serialized_results["results"]:
        content += f"Title: {item['title']}\nURL: {item['url']}\nText: {item['text']}\n\n"
    return content

# Generate an article using OpenAI's GPT model
def generate_article(openai_client, content):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert journalist specializing in writing comprehensive and engaging articles on Chrisitian mainstream churches, how Churches help society, and any related political news. You have a speacial intrest in Chrisitianity and AI too. You look for world Christianity news from the last 14 days, focusing on mainstream Christianity and do not talk about other religions. Use relevant URLs as citations where necessary. All stories should come from different URLs and publications so we get a wide range of sources and stories from accross the world. Look for reputable news outlets and Chrisitian news providers. You audeince are Chrisitians, so always start with positive and uplifting Chrisitian stories first and AI. Your task is to create a well-structured, informative markdown article based solely on the provided news snippets from the last 14 days. Use the given URLs as citations where appropriate to support your writing. Focus on synthesizing the information coherently, highlighting key points, and providing insightful analysis within the context of Chrisitianity. All stories should come from different URLs and publication, examples include reputable news outlets and Chrisitian news providers."},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content

# Save the generated article to a file
def save_article(article, folder, filename='chrisitian_news_article.md'):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    print(colored(f"Markdown article saved to {filepath}", "green"))
    return filepath

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
            {"role": "system", "content": f"You are a professional translator and journalist. Translate and create a well-structured, informative markdown article in {target_language} based on the provided Chrisitian news snippets. Use the given URLs as citations where appropriate. Focus on synthesizing the information coherently, highlighting key points, and providing insightful analysis within the context of the Chrisitian field."},
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
    return filepath

# Prepare the HTML template with logo and author name
def prepare_html_template(language, logo_path, author_name):
    try:
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        print(colored(f"Logo file not found at {logo_path}. Using placeholder text instead.", "yellow"))
        encoded_logo = "Logo not found"

    current_date = datetime.now().strftime("%B %d, %Y")

    return f"""
    <!DOCTYPE html>
    <html lang="{language.lower()[:2]}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI for the Soul: Christianity News & Faith in Technology</title>
        <meta name="description" content="Exploring the latest Christianity news and the intersection of faith and technology">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Lora:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #e2e8f0;
                font-family: 'Inter', sans-serif;
                line-height: 1.8;
            }}
            .content {{
                font-family: 'Lora', serif;
                font-size: 1.1875rem;
                line-height: 2;
                color: #e2e8f0;
            }}
            .content h1 {{
                font-family: 'Inter', sans-serif;
                font-size: 2.5rem;
                font-weight: 800;
                margin-top: 2.5rem;
                margin-bottom: 1rem;
                color: #f8fafc;
                letter-spacing: -0.025em;
            }}
            .content h2 {{
                font-family: 'Inter', sans-serif;
                font-size: 2rem;
                font-weight: 700;
                margin-top: 3rem;
                margin-bottom: 1rem;
                color: #f1f5f9;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #334155;
                letter-spacing: -0.02em;
            }}
            .content h3 {{
                font-family: 'Inter', sans-serif;
                font-size: 1.5rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 0.75rem;
                color: #e2e8f0;
                letter-spacing: -0.015em;
            }}
            .content p {{
                margin-bottom: 1.5rem;
                color: #e2e8f0;
            }}
            .content a {{
                color: #60a5fa;
                text-decoration: none;
                border-bottom: 1px solid #60a5fa;
                transition: all 0.2s ease;
            }}
            .content a:hover {{
                color: #93c5fd;
                border-bottom-color: #93c5fd;
            }}
            .content blockquote {{
                border-left: 4px solid #3b82f6;
                padding-left: 1.5rem;
                margin: 2rem 0;
                font-style: italic;
                color: #94a3b8;
                background: rgba(59, 130, 246, 0.05);
                padding: 1rem 1.5rem;
                border-radius: 0 0.5rem 0.5rem 0;
            }}
            .content ul, .content ol {{
                margin: 1.5rem 0;
                padding-left: 2rem;
            }}
            .content li {{
                margin-bottom: 0.75rem;
                color: #e2e8f0;
            }}
            .content strong {{
                font-weight: 700;
                color: #f1f5f9;
            }}
            .content em {{
                font-style: italic;
                color: #94a3b8;
            }}
            .header-gradient {{
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            .newsletter-card {{
                background: rgba(30, 41, 59, 0.5);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(148, 163, 184, 0.1);
                border-radius: 1rem;
                padding: 2rem;
                margin-bottom: 2rem;
            }}
            @media (max-width: 768px) {{
                .content {{ font-size: 1rem; }}
                .content h1 {{ font-size: 2rem; }}
                .content h2 {{ font-size: 1.5rem; }}
                .content h3 {{ font-size: 1.25rem; }}
                .newsletter-card {{ padding: 1.5rem; }}
            }}
        </style>
    </head>
    <body>
        <header class="header-gradient w-full py-6 mb-8">
            <div class="container mx-auto px-4 sm:px-6 max-w-5xl">
                <div class="flex items-center justify-between">
                    <img src="data:image/png;base64,{encoded_logo}" alt="AI for the Soul Logo" class="h-12 sm:h-16">
                    <nav class="hidden sm:flex space-x-4 items-center">
                        <a href="index.html" class="text-slate-600 hover:text-slate-900 font-medium transition-colors">Latest</a>
                        <a href="archive.html" class="text-slate-600 hover:text-slate-900 font-medium transition-colors">Archive</a>
                        <a href="https://www.aiforthesoul.org/" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">Website</a>
                    </nav>
                </div>
            </div>
        </header>

        <div class="container mx-auto px-4 sm:px-6 py-8 max-w-4xl">
            <div class="newsletter-card">
                <div class="text-center mb-8">
                    <h1 class="text-4xl sm:text-5xl font-bold mb-3 text-white leading-tight">AI for the Soul</h1>
                    <p class="text-xl sm:text-2xl text-blue-300 mb-4 font-light">Christianity News & Faith in Technology</p>
                    <div class="border-t border-slate-600 pt-4 mt-4">
                        <p class="text-2xl font-bold mb-3 text-blue-400">📅 {current_date}</p>
                        <p class="text-lg font-semibold mb-1 text-gray-200">By {author_name}</p>
                        <p class="text-sm text-gray-400">🤖 AI-Generated Newsletter</p>
                    </div>
                </div>
            </div>

            <article class="content">
                <!-- Article content will be inserted here -->
            </article>

            <div class="newsletter-card mt-12">
                <div class="text-center">
                    <h3 class="text-xl font-bold mb-4 text-white">Stay Connected</h3>
                    <p class="text-gray-300 mb-4">For more insights on Christianity and technology, visit our website</p>
                    <a href="https://www.aiforthesoul.org/" class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200">
                        Visit aiforthesoul.org
                    </a>
                    <div class="mt-6 pt-6 border-t border-slate-600">
                        <p class="text-sm text-gray-400">
                            Questions or feedback? Email us at
                            <a href="mailto:support@aiforthesoul.org" class="text-blue-400 hover:text-blue-300">support@aiforthesoul.org</a>
                        </p>
                    </div>
                </div>
            </div>

            <footer class="mt-12 pt-8 border-t border-slate-700 text-center text-gray-400">
                <p class="mb-2 text-sm">&copy; {datetime.now().year} AI for the Soul. All rights reserved.</p>
                <p class="text-xs text-gray-500">
                    This newsletter is automatically generated using AI technology to curate and analyze Christianity news.
                </p>
            </footer>
        </div>
    </body>
    </html>
    """

# Generate an HTML version of the article
def generate_html(markdown_content, language, logo_path, author_name):
    html_template = prepare_html_template(language, logo_path, author_name)

    # Convert markdown to HTML
    html_content = markdown_to_html(markdown_content)

    return html_template.replace("<!-- Article content will be inserted here -->", html_content)

# Convert markdown to HTML
def markdown_to_html(markdown_content):
    # Remove '#' symbols and convert to appropriate HTML tags
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)

    # Convert links
    html_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html_content)

    # Convert bold text
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # Convert italic text
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

    # Convert blockquotes
    html_content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html_content, flags=re.MULTILINE)

    # Convert paragraphs
    html_content = re.sub(r'(?<!\n)\n(?!\n)', r'<br>', html_content)
    html_content = re.sub(r'\n\n', r'</p><p>', html_content)
    html_content = f'<p>{html_content}</p>'

    return html_content

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
    md_filepath = save_translated_article(translated_article, lang.value, folder, f"chrisitian_news_article_{lang.value.lower()[:2]}.md")
    
    # Read the markdown file
    with open(md_filepath, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Generate HTML from markdown
    html_content = generate_html(markdown_content, lang.value, logo_path, author_name)
    save_html_page(html_content, folder, f"chrisitian_news_article_{lang.value.lower()[:2]}.html")

# Main task execution function
def run_task(exa_client, openai_api_key, query, num_results, target_languages, logo_path, author_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = f"chrisitian_news_{timestamp}"
    
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
    logo_path = "AIforthesoul.png"
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
