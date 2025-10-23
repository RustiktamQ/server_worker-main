from fastapi import FastAPI
from controllers.queryСontroller import router as queryRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="db_worker", root_path="/")

origins = ["*"]

# TODO: Временное решение / поменять на проде
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(queryRouter)
