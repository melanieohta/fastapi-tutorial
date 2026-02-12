"""FastAPI main entrypoint file."""

from fastapi import FastAPI, HTTPException, Path, status, Body

from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()


class Post(BaseModel):
    id: Annotated[int, Field()]
    content: Annotated[str, Field()]


# Prepopulate dictionary of posts
posts_db = {
    1: Post(id=1, content="Hello FastAPI!"),
    2: Post(id=2, content="Writing my second post!"),
}


@app.get("/")
def read_root() -> str:
    return "Hello, world!"


@app.get("/about")
def read_about() -> str:
    return "This is a simple HTTP API."


@app.get("/posts")
def list_posts() -> list[Post]:
    return list(posts_db.values())


@app.get("/posts/{post_id}")
def get_post(post_id: Annotated[int, Path(title="ID of Post")]) -> Post:
    if post_id in posts_db:
        return posts_db[post_id]
    raise HTTPException(status_code=404, detail="Post not found")


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Annotated[Post, Body()]):
    if post.id in posts_db:
        raise HTTPException(status_code=400, detail="Post with this ID already exists")
    posts_db[post.id] = post
    return post


@app.put("/posts/{post_id}")
def update_post(
    post_id: Annotated[int, Path()], updated_post: Annotated[Post, Body()]
) -> Post:
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id] = updated_post
    return updated_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: Annotated[int, Path()]) -> None:
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id]
    return None  # 204 = No Content
