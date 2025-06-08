from fastapi import FastAPI
from routers import grades
from routers import llm
from routers import user
from routers import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],           # 这里可替换为你的前端地址，例如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],           # 允许所有请求方法
    allow_headers=["*"],           # 允许所有请求头
)

app.include_router(grades.router)
app.include_router(llm.router)
app.include_router(user.router)
app.include_router(auth.router)