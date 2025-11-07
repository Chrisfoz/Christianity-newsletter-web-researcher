"""
Newsletter Archive Builder for AI for the Soul

This script builds an archive page listing all past newsletters.
It scans for newsletter HTML files and creates an index page.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from termcolor import colored
import base64


def find_newsletter_files(root_dir='.'):
    """Find all newsletter HTML files"""
    newsletters = []

    # Look in timestamped folders
    for folder in Path(root_dir).glob('chrisitian_news_*'):
        if folder.is_dir():
            html_file = folder / 'chrisitian_news_article_en.html'
            if html_file.exists():
                newsletters.append({
                    'path': str(html_file),
                    'folder': folder.name,
                    'date': extract_date_from_folder(folder.name)
                })

    # Look in the newsletter folder
    newsletter_folder = Path(root_dir) / 'newsletter'
    if newsletter_folder.exists():
        html_file = newsletter_folder / 'chrisitian_news_article_en.html'
        if html_file.exists():
            newsletters.append({
                'path': str(html_file),
                'folder': 'newsletter',
                'date': datetime.now()
            })

    # Sort by date, newest first
    newsletters.sort(key=lambda x: x['date'], reverse=True)

    return newsletters


def extract_date_from_folder(folder_name):
    """Extract date from folder name like 'chrisitian_news_20241013_150644'"""
    match = re.search(r'(\d{8})_(\d{6})', folder_name)
    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        try:
            return datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            pass
    return datetime.now()


def extract_title_from_html(html_path):
    """Extract article title from HTML file"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for the main title
            match = re.search(r'<h1[^>]*>(.+?)</h1>', content, re.DOTALL)
            if match:
                title = match.group(1)
                # Remove HTML tags
                title = re.sub(r'<[^>]+>', '', title)
                return title.strip()
    except Exception as e:
        print(colored(f"Error reading {html_path}: {e}", "yellow"))

    return "Christianity Newsletter"


def extract_excerpt_from_html(html_path, max_length=200):
    """Extract first paragraph as excerpt"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for first paragraph in article content
            match = re.search(r'<article[^>]*>.*?<p[^>]*>(.+?)</p>', content, re.DOTALL)
            if match:
                excerpt = match.group(1)
                # Remove HTML tags
                excerpt = re.sub(r'<[^>]+>', '', excerpt)
                # Truncate
                if len(excerpt) > max_length:
                    excerpt = excerpt[:max_length].rsplit(' ', 1)[0] + '...'
                return excerpt.strip()
    except Exception as e:
        print(colored(f"Error reading {html_path}: {e}", "yellow"))

    return "Exploring the latest Christianity news and the intersection of faith and technology."


def build_archive_page(newsletters, logo_path='AIforthesoul.png'):
    """Build the archive HTML page"""

    # Encode logo
    try:
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        print(colored(f"Logo file not found at {logo_path}", "yellow"))
        encoded_logo = ""

    # Build newsletter cards
    newsletter_cards = []
    for i, newsletter in enumerate(newsletters):
        title = extract_title_from_html(newsletter['path'])
        excerpt = extract_excerpt_from_html(newsletter['path'])
        date_str = newsletter['date'].strftime('%B %d, %Y')

        # Create a clean URL for the newsletter
        if newsletter['folder'] == 'newsletter':
            url = 'index.html'
            badge = '<span class="bg-blue-500 text-white text-xs px-2 py-1 rounded ml-2">Latest</span>'
        else:
            url = f"{newsletter['folder']}/chrisitian_news_article_en.html"
            badge = ''

        card_html = f'''
            <div class="newsletter-card hover:border-blue-500 transition-all duration-200">
                <div class="flex justify-between items-start mb-2">
                    <h2 class="text-2xl font-bold text-white">{date_str}</h2>
                    {badge}
                </div>
                <p class="text-gray-300 mb-4 leading-relaxed">{excerpt}</p>
                <a href="{url}" class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded transition-colors duration-200">
                    Read Newsletter →
                </a>
            </div>
        '''
        newsletter_cards.append(card_html)

    cards_html = '\n'.join(newsletter_cards)

    # Build full HTML
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter Archive - AI for the Soul</title>
        <meta name="description" content="Browse past issues of the AI for the Soul Christianity newsletter">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #e2e8f0;
                font-family: 'Inter', sans-serif;
                min-height: 100vh;
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
                .newsletter-card {{ padding: 1.5rem; }}
            }}
        </style>
    </head>
    <body>
        <header class="header-gradient w-full py-6 mb-8">
            <div class="container mx-auto px-4 sm:px-6 max-w-5xl">
                <div class="flex items-center justify-between">
                    <img src="data:image/png;base64,{encoded_logo}" alt="AI for the Soul Logo" class="h-12 sm:h-16">
                    <nav class="hidden sm:flex space-x-4">
                        <a href="index.html" class="text-slate-600 hover:text-slate-900 font-medium">Latest</a>
                        <a href="archive.html" class="text-blue-600 hover:text-blue-800 font-medium">Archive</a>
                    </nav>
                </div>
            </div>
        </header>

        <div class="container mx-auto px-4 sm:px-6 py-8 max-w-4xl">
            <div class="text-center mb-12">
                <h1 class="text-4xl sm:text-5xl font-bold mb-3 text-white">Newsletter Archive</h1>
                <p class="text-xl text-gray-300">Browse past issues of AI for the Soul</p>
            </div>

            <div class="space-y-6">
                {cards_html}
            </div>

            {'' if newsletter_cards else '<div class="newsletter-card text-center"><p class="text-gray-400">No newsletters published yet. Check back soon!</p></div>'}

            <div class="mt-12 text-center">
                <a href="https://www.aiforthesoul.org/" class="text-blue-400 hover:text-blue-300 font-medium">
                    Visit aiforthesoul.org →
                </a>
            </div>

            <footer class="mt-12 pt-8 border-t border-slate-700 text-center text-gray-400">
                <p class="mb-2 text-sm">&copy; {datetime.now().year} AI for the Soul. All rights reserved.</p>
            </footer>
        </div>
    </body>
    </html>
    '''

    return html


def main():
    """Main function to build archive"""
    print(colored("Building newsletter archive...", "cyan"))

    # Find all newsletters
    newsletters = find_newsletter_files()
    print(colored(f"Found {len(newsletters)} newsletters", "green"))

    # Build archive page
    archive_html = build_archive_page(newsletters)

    # Save archive page
    with open('archive.html', 'w', encoding='utf-8') as f:
        f.write(archive_html)

    print(colored("✓ Archive page saved to archive.html", "green"))

    # Also update navigation in latest newsletter if it exists
    if os.path.exists('index.html'):
        print(colored("✓ Latest newsletter available at index.html", "green"))

    return 0


if __name__ == '__main__':
    exit(main())
