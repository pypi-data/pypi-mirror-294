import logging as log
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Span, Text

console = Console(style="bold white on cyan1", soft_wrap=True)
blue_console = Console(style="bold white on blue", soft_wrap=True)
print = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="red", overflow="fold")) for arg in args), **kwargs) # noqa
print_bold = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="bold", overflow="fold")) for arg in args), **kwargs)
input = lambda arg, **kwargs: Confirm.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, default="y", **kwargs) # noqa
ask = lambda arg, **kwargs: Prompt.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, **kwargs) # noqa

def is_valid_url(url) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def html_to_markdown(soup, base_url=None):
    """Convert HTML content to Markdown format."""
    markdown = []

    for element in soup.descendants:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            markdown.append(f"{'#' * level} {element.get_text(strip=True)}\n")
        elif element.name == 'p':
            markdown.append(f"{element.get_text(strip=True)}\n")
        elif element.name == 'pre':
            code = element.find('code')
            if code:
                markdown.append(f"```\n{code.get_text(strip=True)}\n```\n")
        elif element.name == 'ul':
            for li in element.find_all('li'):
                markdown.append(f"- {li.get_text(strip=True)}\n")
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li'), 1):
                markdown.append(f"{i}. {li.get_text(strip=True)}\n")
        elif element.name == 'a':
            href = element.get('href', '')
            text = element.get_text(strip=True)
            markdown.append(f"[{text}]({href})")
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '')
            markdown.append(f"![{alt}]({src})")

    return '\n'.join(markdown).strip()

def browse(urls, timeout=25, interactive=False):
    log.debug(f"browse function called with urls: {urls}, timeout: {timeout}, interactive: {interactive}")
    results = []
    for i, url in enumerate(urls):
        try:
            log.debug(f"Sending GET request to {url}")
            response = requests.get(url, timeout=timeout)
            log.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html5lib')

            title = soup.title.string if soup.title else "No title found"
            
            # Extract the main content
            main_content = soup.find('div', class_='markdown-body')
            if not main_content:
                main_content = soup.find('div', id='readme')
            if not main_content:
                main_content = soup.find('article')
            if not main_content:
                main_content = soup.find('main')
            if not main_content:
                main_content = soup.body

            markdown_content = html_to_markdown(main_content, base_url=url) if main_content else "Could not find main content"
            log.debug(f"Main content HTML: {main_content.prettify()[:200]}...")  # Log the first 200 characters of the main content HTML
            log.debug(f"Markdown content: {markdown_content[:200]}...")  # Log the first 200 characters for debugging
            
            # Clean up the markdown content
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)  # Remove excessive newlines
            markdown_content = re.sub(r'^\s+|\s+$', '', markdown_content, flags=re.MULTILINE)  # Trim leading/trailing whitespace
            
            result = {
                'url': url,
                'title': title,
                'content': markdown_content,
            }
            results.append(result)
            
            log.info(f"Processed: {url}")
        except requests.exceptions.RequestException as e:
            log.error(f"Error fetching the webpage {url}: {str(e)}")
            error_message = f"Error fetching the webpage: {e.response.status_code if hasattr(e, 'response') else str(e)}"
            results.append({
                'url': url,
                'error': error_message,
            })
        except Exception as e:
            log.error(f"Unexpected error while browsing {url}: {str(e)}")
            log.exception("Exception traceback:")
            results.append({
                'url': url,
                'error': f"Error browsing {url}: {str(e)}",
            })
    
    return results

if __name__ == "__main__":
    # Example usage
    pass
