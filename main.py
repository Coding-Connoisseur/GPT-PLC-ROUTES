from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import shell, files, code, system, monitor, git, package, apps, refactor, batch, plc, radio

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(shell.router, prefix="/shell")
app.include_router(files.router, prefix="/files")
app.include_router(code.router, prefix="/code")
app.include_router(system.router, prefix="/system")
app.include_router(monitor.router, prefix="/monitor")
app.include_router(git.router, prefix="/git")
app.include_router(package.router, prefix="/package")
app.include_router(apps.router, prefix="/apps")
app.include_router(refactor.router, prefix="/refactor")
app.include_router(batch.router, prefix="/batch")
app.include_router(plc.router, prefix="/plc")
app.include_router(radio.router, prefix="/radio")


@app.get("/debug/routes")
def list_routes():
    from fastapi.routing import APIRoute
    return [{
        "path": route.path,
        "name": route.name,
        "methods": route.methods
    } for route in app.routes if isinstance(route, APIRoute)]