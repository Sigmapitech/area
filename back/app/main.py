from fastapi import FastAPI
import uvicorn


app = FastAPI(redoc_url="/api/doc", docs_url=None)


def main():
    uvicorn.run(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
