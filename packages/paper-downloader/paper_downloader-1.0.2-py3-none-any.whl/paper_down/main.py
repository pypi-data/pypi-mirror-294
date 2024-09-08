import os
from prompt_toolkit import PromptSession
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import radiolist_dialog
import shutil
from paper_down.downloader import download_and_merge_pdfs
from paper_down.save import fetch_paper_types


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL Validator
class URLValidator(Validator):
    def __init__(self, required=True) -> None:
        super().__init__()
        self.required = required

    def validate(self, document):
        text = document.text
        if self.required:
            if not text.startswith("http"):
                raise ValidationError(message="URL must start with http or https", cursor_position=len(text))
        else:
            if text != "":
                if not text.startswith("http"):
                    raise ValidationError(message="URL must start with http or https", cursor_position=len(text))

class InfoValidator(Validator):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type
    def validate(self, document: Document) -> None:
        text = document.text.strip()
        if text == "":
            raise ValidationError(message=f"{self.type} should not be empty", cursor_position=len(text))

def compose_filename(attributes, order=["venue", "title", "author"]):
    filename = ""
    for idx, key in enumerate(order):
        filename += attributes[key]
        if idx != len(order) - 1:
            filename += "_"
    filename += ".pdf"
    return filename

# Function to show a single-choice (radio list) menu
def main():
    session = PromptSession()

    # Define style for the prompt
    style = Style.from_dict({
        'prompt': 'ansicyan bold',
        '': '#ffffff',
        'title': 'bold ansiblue',
        'warning': 'bold ansired',
        'success': 'bold ansigreen',
    })

    # Ask for the first URL
    confirm = False
    url1 = None 
    url2 = None
    title = None
    author = None
    venue = None
    while(not confirm):
        clear_screen()
        print_formatted_text(HTML('<title>✨ Welcome to the PDF Downloader ✨</title>'))
        url1 = session.prompt(
            HTML('<prompt>🌐 Enter the first URL (required): </prompt>'), 
            validator=URLValidator(required=True), 
            style=style,
            default=url1 or ""
        )

        # Ask for the second URL (optional)
        url2 = session.prompt(
            HTML('<prompt>🌐 Enter the second URL (optional, press Enter to skip): </prompt>'), 
            validator=URLValidator(required=False), 
            style=style, 
            default=url2 or ""
        )
        title = session.prompt(
            HTML('<prompt>👤 Enter the title: </prompt>'), 
            style=style,
            validator=InfoValidator('Title'),
            default=title or ""
        )
        author = session.prompt(
            HTML('<prompt>👤 Enter the author name: </prompt>'), 
            style=style, 
            validator=InfoValidator('Author'),
            default=author or ""
        )
        venue = session.prompt(
            HTML('<prompt>👤 Enter the venue: </prompt>'), 
            style=style, 
            validator=InfoValidator('Venue'), 
            default=venue or ""
        )

        attributes = {
            "venue": venue,
            "title": title,
            "author": author,
        }
        filename = compose_filename(attributes)
        save_to = radiolist_dialog(
            title="Choose where to save",
            text="Which domain dose this paper belongs to?",
            values=fetch_paper_types()
        ).run()
        filename = os.path.join(save_to, filename)

        if not url2:
            url2 = None

        # Ask user confirmation before starting download
        confirm = yes_no_dialog(
            title="Start Download?",
            text=f"You're about to download PDF from:\n\n1. {url1}\n" + \
                (f"2. {url2}\n" if url2 else "") + \
                f"Venue: {venue}\n" + \
                f"Title: {title}\n" + \
                f"Authors: {author}\n" + \
                f"Filename: {filename}\n\n" + \
                "Proceed?"
        ).run()

    if confirm:
        try:
            # Run the download in the terminal environment
            temp_filename = download_and_merge_pdfs(url1, url2)
            shutil.move(temp_filename, filename)
            if os.path.exists(temp_filename):
                shutil.rmtree(temp_filename)
            message_dialog(title="Download Completed", text=f"Download of PDF(s) completed successfully to {filename}.").run()
        except Exception as e:
            message_dialog(title="Error", text=f"<warning>{str(e)}</warning>").run()
            raise e
    else:
        message_dialog(title="Cancelled", text="Operation was cancelled by the user.").run()

if __name__ == "__main__":
    main()
