from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
import koco_product_sqlmodel.fastapi.routes.catalog as rcat
import koco_product_sqlmodel.fastapi.routes.security as rsec

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="src/koco_product_sqlmodel/fastapi/static"), name="static")
FAVICON_PATH="src/koco_product_sqlmodel/fastapi/static/img/favicon.ico"

app.include_router(rcat.router, prefix="/catalogs")
app.include_router(rsec.router, prefix="/auth")

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/html/index.html")

@app.get("/favicon.ico",  include_in_schema=False)
async def serve_favicon():
    return FileResponse(path=FAVICON_PATH)

def main():
    pass

if __name__=="__main__":
    main()