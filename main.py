from datetime import date, datetime
from typing import Union
import urllib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import os

POSTS_PER_PAGE = 5
POSTS_FODLER = "posts"
BREWING_FOLDER = "brewing"
TAGS_FILE = "tags.txt"

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://ganymede.ch",
    "https://dev.ganymede.ch"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    title: str
    tags: list[str]
    html: str
    date: str


def read_post_data(post):
    with open(os.path.join(POSTS_FODLER, post)) as f:
        title = f.readline()
        tags = f.readline().split(",")
        html = f.read()
    return {"title": title, "tags": tags, "html": html, "date": post.split(".")[0]}


def get_page_count(posts):
    return math.ceil(len(posts) / POSTS_PER_PAGE) 


def get_post_tags():
    tags = dict()
    with open(TAGS_FILE) as f:
        for l in f:
            tags_data = l.split(":")
            tags[tags_data[0]] = tags_data[1].strip().split(",")
    return tags

def get_post_files(tag):
    tag = urllib.parse.unquote(tag, encoding='utf-8', errors='replace')
    if(tag and tag != "all"):
        return get_post_tags().get(tag, [])
    else:
        return os.listdir(POSTS_FODLER)

@app.get("/posts/page_count")
def posts_count(tag: Union[str, None] = None):
    files = get_post_files(tag)
    return get_page_count(files)


@app.get("/posts/page/{page}")
def posts_page(page: int, tag: Union[str, None] = None):
    files = get_post_files(tag)
    files = sorted(files, reverse=True)
    if page < 0 or page >= get_page_count(files):
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = page * POSTS_PER_PAGE
    return [
        read_post_data(path) for path in files[start_idx : (start_idx + POSTS_PER_PAGE)]
    ]


@app.get("/posts/tags")
def posts_tags():
    return list(get_post_tags().keys())

@app.get("/languages/{lang}")
def kiswahili(lang:str):
    try:
        with open("languages/"+lang+".txt") as f:
            return f.read()
    except:
        raise HTTPException(status_code=404, detail="Language File not Found")

@app.get("/brewing")
def brewing_count():
    posts = []
    try:
        for filename in  sorted(os.listdir(BREWING_FOLDER), reverse=True):
            with open(os.path.join(BREWING_FOLDER, filename)) as f:
                title = f.readline()
                posts.append({"title": title, "content": f.read()})
    except:
        raise HTTPException(status_code=404, detail="Brewing Files could not be read")          
    
    return posts
        
