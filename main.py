from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text
from datetime import datetime
from uuid import uuid4 as uuid

#
class Post(BaseModel):
    id: str
    titulo: str
    autor: str
    contenido: Text
    fecha: datetime = datetime.now()


posts = []
app = FastAPI()


@app.get('/')
def read_raiz():
    return {"mensaje": "hola desde mi API restful"}


@app.get('/posts')
def obtener_posts():
    return posts


@app.post('/posts')
def grabar_posts(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]


@app.get('/posts/{post_id}')
def leer_posts(post_id: str):
    if not isinstance(post_id, str):
        raise HTTPException(status_code=400, detail="El ID del post debe ser una cadena de texto")
    
    post = next((post for post in posts if post["id"] == post_id), None)
    
    if post is None:
        raise HTTPException(status_code=404, detail="post no encontrado")
    
    return post


@app.delete('/posts/{post_id}')
def eliminar_posts(post_id: str):
    post = next((post for post in posts if post["id"] == post_id), None)
    
    if post is None:
        raise HTTPException(status_code=404, detail="post no encontrado")
    
    posts.remove(post)
    return {"mensaje": "El post se ha eliminado correctamente"}


@app.put('/posts/{post_id}')
def actualizar_posts(post_id: str, updatedPost: Post):
    post = next((post for post in posts if post["id"] == post_id), None)
    
    if post is None:
        raise HTTPException(status_code=404, detail="post no encontrado")
    
    post.update(updatedPost.dict())
    return {"mensaje": "El post se ha actualizado correctamente"}
