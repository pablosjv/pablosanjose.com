
import hashlib
import logging
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import requests
from jinja2 import Environment, FileSystemLoader

from notion.block import (BulletedListBlock, CalloutBlock, CodeBlock, DividerBlock, EquationBlock, HeaderBlock,
                          ImageBlock, NumberedListBlock, QuoteBlock, SubheaderBlock, SubsubheaderBlock, TextBlock,
                          TodoBlock, ToggleBlock)
from notion.client import NotionClient

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S'
)


@dataclass
class Page():
    title: str
    slug: str = ""
    date: datetime.date = datetime.now()
    tags: List[str] = field(default_factory=list)
    city: str = ""
    draft: bool = False
    math: bool = False
    filename: str = field(init=False)
    blocks: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.slug:
            self.filename = self.title.lower().replace(' ', '-')
        else:
            self.filename = self.slug


def download_image(
        url: str,
        image_folder: str = 'public/images',
        parent_folder: str = 'static'):
    file_name_hash = hashlib.sha256(
        urlparse(url).path.encode('utf-8')).hexdigest()
    file_path = f'{parent_folder}/{image_folder}/{file_name_hash}.png'
    reference_file_path = f'/{image_folder}/{file_name_hash}.png'
    os.makedirs(f'{parent_folder}/{image_folder}', exist_ok=True)
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    return reference_file_path


def generate_image_block(image_block: ImageBlock):
    caption = image_block.caption.replace('"', '\\"')
    image_folder = image_block.parent.title.lower().replace(' ', '-')
    image_folder = f"public/images/{image_folder}"
    reference_image_file = download_image(image_block.source, image_folder)
    # NOTE: double scape brackets to get {{ ... }}
    return f'\n{{{{< figure caption="{caption}" src="{reference_image_file}" >}}}}\n'


def generate_code_block(code_block: CodeBlock):
    return f'\n```{code_block.language.lower()}\n{code_block.title}\n```\n'


def generate_text_block(text_block: TextBlock):
    return f'\n{text_block.title}\n'


def generate_bulleted_list(bulleted_list: BulletedListBlock):
    return f'* {bulleted_list.title}'


def generate_numbered_list(numbered_list: NumberedListBlock):
    return f'1. {numbered_list.title}'


def generate_todo_block(todo_block: TodoBlock):
    check = 'x' if todo_block.checked else ' '
    return f'- [{check}] {todo_block.title}'


def generate_header_block(header_block: HeaderBlock):
    return f"\n# {header_block.title}\n"


def generate_subheader_block(subheader_block: SubheaderBlock):
    return f"\n## {subheader_block.title}\n"


def generate_subsubheader_block(subsubheader_block: SubsubheaderBlock):
    return f"\n### {subsubheader_block.title}\n"


def generate_divider_block(divider_block: DividerBlock):
    return "\n---\n"


def generate_toggle_block(toggle_block: ToggleBlock):
    text = f"\n- {toggle_block.title}"
    for b in toggle_block.children:
        text += f" \n   {block_parse_func[b.type](b)}"
    return text


def generate_quote_block(quote_block: QuoteBlock):
    return f"\n> {quote_block.title}\n"


def generate_callout_block(callout_block: CalloutBlock):
    return f"\n> {callout_block.icon} {callout_block.title}\n"

def generate_equation(equation_block: EquationBlock):
    return f"\n$$$\n{equation_block.title}\n$$$\n"


# NOTE: implement using pattern matching
block_parse_func = {
    "text": generate_text_block,
    "image": generate_image_block,
    "code": generate_code_block,
    "bulleted_list": generate_bulleted_list,
    "numbered_list": generate_numbered_list,
    "header": generate_header_block,
    "sub_header": generate_subheader_block,
    "sub_sub_header": generate_subsubheader_block,
    "to_do": generate_todo_block,
    "divider": generate_divider_block,
    "toggle": generate_toggle_block,
    "quote": generate_quote_block,
    "callout": generate_callout_block,
    "equation": generate_equation,
}


def save_content(page: Page, entry_type: str = 'post'):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(f'{entry_type}.md.j2')
    output_from_parsed_template = template.render(page=page)
    conten_paths = {
        'post': 'content/posts',
        'page': 'content',
    }
    with open(f"{conten_paths[entry_type]}/{page.filename}.md", "w") as f:
        f.write(output_from_parsed_template)


def main():
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    NOTION_ORG = os.getenv('NOTION_ORG')
    BLOG_COLLECTION_ID = os.getenv('BLOG_COLLECTION_ID')
    BLOG_COLLECTION_VIEW_ID = os.getenv('BLOG_COLLECTION_VIEW_ID')
    OTHER_COLLECTION_ID = os.getenv('OTHER_COLLECTION_ID')
    OTHER_COLLECTION_VIEW_ID = os.getenv('OTHER_COLLECTION_VIEW_ID')

    client = NotionClient(token_v2=NOTION_TOKEN)

    logging.info('Querying blog database')
    cv = client.get_collection_view(
        f"https://www.notion.so/{NOTION_ORG}/{BLOG_COLLECTION_ID}?v={BLOG_COLLECTION_VIEW_ID}",
    )
    database_records = cv.default_query().execute()
    for record in database_records:
        logging.info(f'Geting record: {record.title}')
        if not record.title:
            logging.info("Emtpy record. Consider removing it")
            continue
        page = Page(
            title=record.title,
            slug=record.slug,
            date=record.date.start,
            tags=record.tags,
            draft=record.draft,
            math=record.math,
            city=record.city,
        )
        for block in record.children:
            if block.type not in block_parse_func:
                logging.warning(f'No implemented {block}')
                logging.warning(block.type)
            else:
                block_text = block_parse_func[block.type](block)
                page.blocks.append(block_text)
        save_content(page, entry_type='post')

    logging.info('Querying other pages database')
    cv = client.get_collection_view(
        f"https://www.notion.so/{NOTION_ORG}/{OTHER_COLLECTION_ID}?v={OTHER_COLLECTION_VIEW_ID}")
    database_records = cv.default_query().execute()
    for record in database_records:
        logging.info(f'Geting record: {record.title}')
        page = Page(
            title=record.title
        )
        for block in record.children:
            block_text = block_parse_func[block.type](block)
            page.blocks.append(block_text)
        save_content(page, entry_type='page')


if __name__ == '__main__':
    main()
