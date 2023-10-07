import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api import router

app = FastAPI(title="KV Store", version="0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    print(exc)
    raise HTTPException(status_code=500, detail="internal server error")
    # return JSONResponse(
    #     status_code=418,
    #     content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    # )


app.include_router(router, prefix="/api/v1/values")

if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=5000,
        reload=True
    )
