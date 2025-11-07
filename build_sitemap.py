"""
Sitemap Generator for AI for the Soul Newsletter

Generates an XML sitemap for better SEO.
"""

import os
from datetime import datetime
from pathlib import Path
from termcolor import colored


def find_html_pages(root_dir='.'):
    """Find all public HTML pages"""
    pages = []

    # Main pages
    if os.path.exists('index.html'):
        pages.append({
            'url': '',
            'priority': '1.0',
            'changefreq': 'weekly',
            'lastmod': datetime.now()
        })

    if os.path.exists('archive.html'):
        pages.append({
            'url': 'archive',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': datetime.now()
        })

    # Newsletter folders
    for folder in Path(root_dir).glob('chrisitian_news_*'):
        if folder.is_dir():
            html_file = folder / 'chrisitian_news_article_en.html'
            if html_file.exists():
                # Get modification time
                mtime = datetime.fromtimestamp(html_file.stat().st_mtime)
                pages.append({
                    'url': f'{folder.name}/chrisitian_news_article_en.html',
                    'priority': '0.6',
                    'changefreq': 'monthly',
                    'lastmod': mtime
                })

    return pages


def build_sitemap(pages, base_url='https://html-starter-ko9cvrztp-christopher-foster-mcbrides-projects.vercel.app'):
    """Build XML sitemap"""

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in pages:
        url = f"{base_url}/{page['url']}" if page['url'] else base_url
        lastmod = page['lastmod'].strftime('%Y-%m-%d')

        xml += '  <url>\n'
        xml += f'    <loc>{url}</loc>\n'
        xml += f'    <lastmod>{lastmod}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>'

    return xml


def main():
    """Main function"""
    print(colored("Building sitemap...", "cyan"))

    pages = find_html_pages()
    print(colored(f"Found {len(pages)} pages", "green"))

    sitemap_xml = build_sitemap(pages)

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    print(colored("✓ Sitemap saved to sitemap.xml", "green"))

    return 0


if __name__ == '__main__':
    exit(main())
