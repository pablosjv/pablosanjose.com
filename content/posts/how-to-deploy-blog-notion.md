---
title: "How I deployed my personal blog with Vercel + Hugo + Github Actions + Notion"
date: 2021-02-19
draft: false
slug: how-to-deploy-blog-notion
city: Madrid
toc: true
tags:
- tutorial
- dev
- web
---


It's been a while since I started about having a website of my own. My goal always has been modest: host a small portfolio, blog, and resume.

 I bought my domain a little over a year ago but I never got into it. Lately, I decided to start building my own website. 

## Let's see how to host

A static website was enough for my needs so I research about different platforms and technologies to generate the content and host it. 

Soon enough I found [Vercel](https://vercel.com/). The features and the simplicity really sell me out. Researching more about it, I found this interesting [site](https://notion-blog.now.sh/), made with [Notion](https://www.notion.so/)! This was a brilliant idea. Notion is one of those tools that I love and I highly recommend it for everybody. See that I could integrate the content of a website with Notion really inspired me. I started to research more and I found more [blog posts](https://dev.to/kojikanao/set-up-a-blog-with-notion-and-vercel-in-10-min-4nb1) about it.

The original website used Next.js to build the blog. I am not very skilled with javascript and neither with frontend frameworks. For me, using a static site generator is the way to go. I used [Hugo](https://gohugo.io/) in the pasts and it worked very well with almost plain markdown files and little configuration. It is also supported on Vercel out of the box so the decision is made. What I needed to do is to extract the Notion pages as markdowns files and put them into a github repository so it 

## Notion API

Notion has been promising an API for a while, but it seems it will never come. Luckily there are a number of unofficial APIs that we can use.

I soon found a [Go API](https://github.com/kjk/notionapi) client, thanks that the creator also made a [blog with notion](https://github.com/kjk/blog). I used go before so I decided to gave it a try. I also quickly found the [Carlos Becker's Blog](https://github.com/caarlos0/carlosbecker.com), which used the same idea. His project gave the template I need to start coding my way through the API.

Unfortunately, I really struggle to understand the Go API. I have to say that my skills in go are not as good as I though. I take some learnings from that and go to investigate the [Python API](https://github.com/jamalex/notion-py). I am way more familiar with python and I think this API is quite simple to use.

The idea was simple, first we need the credentials to call the unofficial API. This can be obtained opening the developer tools in your Notion workspace webpage and looking for the `token_v2` cookie. I store it in a environment variable and start using the Notion Python Client


```python
import os
from notion.client import NotionClient

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
client = NotionClient(token_v2=NOTION_TOKEN)
```


Then, I need to create a database in Notion to store the content and get its url. The db url is composed of several things: the notion host (obviously), the organization (your username in a personal account), the database or collection identifier and the database view identifier. I did the same and put all of this things in environment variables and construct the url to get the pages


```python
cv = client.get_collection_view(
    f"https://www.notion.so/{NOTION_ORG}/{OTHER_COLLECTION_ID}?v={OTHER_COLLECTION_VIEW_ID}")
database_records = cv.default_query().execute()
```


You can do more complex queries using filters. It is in the API documentation. For now, this is sufficient.

The response is a list of notion pages objects. Let's see how we can extract those pages.

## Getting the content

Firs, I created a custom `Page` dataclass to encapsulate everything


```python
@dataclass
class Page():
    title: str
    slug: str = ""
    date: datetime.date = datetime.now()
    tags: List[str] = field(default_factory=list)
    city: str = ""
    draft: bool = False
    filename: str = field(init=False)
    blocks: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.slug:
            self.filename = self.title.lower().replace(' ', '-')
        else:
            self.filename = self.slug
```


Each one of the attributes of the class is a field in the database with the except of:

* `filename`: this is the name of the file to store the page. Titles can be long and have inconvenient symbols, so by default we will use the `slug` field.

* `blocks`: This will be a list with the block contents of the page. A block is the basic unit in Notion. We will need to extract each block of the database and transform it to some kind of string representation in markdown to be rendered by Hugo. We will get more into that later.

We can iterate through the previous pages list to extract the each page and its contents into our custom class. We need to iterate again for the children in the page to update the `blocks` fields


```python
for record in database_records:
    if not record.title:  # Empty record, we skip it
        continue
    page = Page(
        title=record.title,
        slug=record.slug,
        date=record.date.start,
        tags=record.tags,
        draft=record.draft,
        city=record.city,
    )
		for block in record.children:
			  page.blocks.append(block_text)
```


We are making progress! However we are not done. As I said before, this blocks are just python objects right now with the page block contents. We need to translate them somehow to markdown. In this case I went with the dum and simple route. For each type of block, I implemented a custom function that generates the markdown content. There are quite a few of them some let's see a couple of them


```python
def generate_code_block(code_block: CodeBlock):
    return f'\n```{code_block.language}\n{code_block.title}\n```\n'


def generate_text_block(text_block: TextBlock):
    return text_block.title


def generate_bulleted_list(bulleted_list: BulletedListBlock):
    return f'* {bulleted_list.title}'
```


Then I created the following dictionary mapping


```python
block_parse_func = {
    "text": generate_text_block,
    "image": generate_image_block,
    "code": generate_code_block,
    "bulleted_list": generate_bulleted_list,
    "numbered_list": generate_numbered_list,
    "header": generate_header_block,
    "sub_header": generate_subheader_block,
    "sub_sub_header": generate_subsubheader_block,
    "quote": generate_quote_block,
}
```


An our previous snippet will be like this


```python
for record in database_records:
    if not record.title:
        continue
    page = Page(
        title=record.title,
        slug=record.slug,
        date=record.date.start,
        tags=record.tags,
        draft=record.draft,
        city=record.city,
    )
    for block in record.children:
        if block.type not in block_parse_func:
						# type not implemented
						continue
        else:
            block_text = block_parse_func[block.type](block)
            page.blocks.append(block_text)
```


Now we have the page contents in markdown! You can see more details for the implementation in the [repository](https://github.com/pablosjv/pablosanjose.com), including how I handled downloading images.

## Making a template

Finally, we kist need to save the contents to a file. I used a small jinja template to create the blog posts


```python
---
title: "{{ page.title }}"
date: {{ page.date }}
draft: {{ page.draft | string | lower }}
slug: {{ page.slug }}
city: {{ page.city }}
toc: true
tags:
{%- for tag in page.tags %}
- {{ tag }}
{% endfor %}
---

{% for content_block in page.blocks %}
{{ content_block }}
{% endfor %}
```


This template is expecting our previous `Page` object and will create the Hugo page. The following code with save our templated file


```python
def save_content(page: Page):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(f'post.md.j2')
    output_from_parsed_template = template.render(page=page)
    with open(f"content/posts/{page.filename}.md", "w") as f:
        f.write(output_from_parsed_template)
```


Easy!

## Putting it together

I created a small script in python to store all this code, a small [`requirements.txt`](https://github.com/pablosjv/pablosanjose.com/blob/main/requirements.txt) file, and setup the repository with a simple [`Makefile`](https://github.com/pablosjv/pablosanjose.com/blob/main/Makefile). Let's run our code


```shell
❯ make refresh
2021-02-19 03:37:54 - INFO: Querying blog database
2021-02-19 03:37:55 - INFO: Geting record: My blog is live!
...
❯ ls content/posts
my-blog-is-live.md
```


{{< figure caption="" src="/public/images/how-i-deployed-my-personal-blog-with-vercel-+-hugo-+-github-actions-+-notion/5c6be9990e1ffe1be2588a474967828afe972d8c9637f658ecdc18590520fd3b.png" >}}

## Continuous deployment

Vercel handles the integration with Github seamlessly. Just with a couple of clicks the page was deployed. It also supports the preview of branches and pull request. It is an amazing product. The only modification I needed to do is add the Hugo version with a config file in the repo as the default one quite low


```json
{
    "build": {
        "env": {
            "HUGO_VERSION": "0.80.0"
        }
    }
}
```


Taking again inspiration (or at this point, straight copy) from [Carlos Becker's Website](https://github.com/caarlos0/carlosbecker.com) , I set up a Github actions workflow on a schedule so the content is refreshed daily.

## And we are live!

If you are reading this it means that everything I said worked as expected. Let's start writing 🙂
