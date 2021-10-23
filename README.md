# [pablosanjose.com](https://pablosanjose.com)

![GitHub last commit](https://img.shields.io/github/last-commit/pablosjv/pablosanjose.com?logo=hey)
![Build Workflow Status](https://img.shields.io/github/workflow/status/pablosjv/pablosanjose.com/build)

Source code for the static website [pablosanjose.com](https://pablosanjose.com), where I host my resume and other stuff.

Posts actually are written on [Notion](https://notion.so) and synced to markdown
using the unofficial python api. Check `refresh.py` to see how it's done.

## Acknowledgements

I was only able to do this project with the inspiration of the following ones

- [carlosbecker.com](https://github.com/caarlos0/carlosbecker.com)
- [kjk/blog](https://github.com/kjk/blog)
- [notion-blog](https://notion-blog.now.sh/)
- [notion-py](https://github.com/jamalex/notion-py)

## Configuration

The notion databases have the following structure in the url:

```jinja
https://www.notion.so/{{NOTION_ORG}}/{{DB_ID}}?v={{DB_VIEW_ID}}
```

This project needs the following configuration variables:

- `NOTION_TOKEN`: authorization token that can be obtained from the value in `token_v2` cookie. This cookie expires and you will have to renew it for the pipeline to work again
- `BLOG_COLLECTION_ID`: the DB_ID to get the entries for the blog.
- `BLOG_COLLECTION_VIEW_ID`: the DB_VIEW_ID for the blog. The actual view is not relevant, but the value is needed for the queries to work properly.
- `OTHER_COLLECTION_ID`: the DB_ID to get the entries for other pages. This pages include the `about me` section
- `OTHER_COLLECTION_VIEW_ID`: the DB_VIEW_ID for the blog.
- `NOTION_ORG`: value of your NOTION_ORG. For personal accounts, it is your username in lowercase and without spaces.
