from fastapi import FastAPI
from api import router
import webbrowser
from fastapi import FastAPI

app= FastAPI()
app.include_router(router.info)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="192.168.1.39", port=4000, log_level="info", reload=True)
    webbrowser.open("http://192.168.1.39:4000")