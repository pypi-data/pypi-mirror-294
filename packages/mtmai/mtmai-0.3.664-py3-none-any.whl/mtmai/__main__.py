import argparse
import asyncio
import json
import logging
import sys
import threading
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates

from mtmai.core import coreutils

sys.path.insert(
    0, str(Path(f"{Path(__file__).resolve().parent}/../../mtmtrain").resolve())
)
sys.path.insert(
    0, str(Path(f"{Path(__file__).resolve().parent}/../../mtmlib").resolve())
)
sys.path.insert(
    0, str(Path(f"{Path(__file__).resolve().parent}/../../mtmdb").resolve())
)


from mtmai.api.main import api_router
from mtmai.api.routes import home
from mtmai.core.__version__ import version
from mtmai.core.config import settings
from mtmai.core.coreutils import is_in_gitpod, is_in_testing, is_in_vercel
from mtmai.core.logging import setup_logging
from mtmai.core.seed import init_database

setup_logging()
load_dotenv()
logger = logging.getLogger()


def try_get_version():
    import importlib.metadata

    # 替换 'your-package-name' 为你的包名
    version = importlib.metadata.version("mtmai")
    print(version)


logger.info("版本号V2: %s", try_get_version())
logger.info(
    f"[🚀🚀🚀 mtmai]({settings.VERSION})"  # noqa: G004
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if is_in_gitpod() and not is_in_testing():
        init_database()
        export_to = "mtmai/mtmai/openapi.json"
        openapi = app.openapi()
        with Path.open(export_to, "w") as f:
            logger.info(
                "openapi.json exported %s to %s",
                openapi.get("openapi", "unknown version"),
                export_to,
            )
            json.dump(openapi, f, indent=2)
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    if len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    return f"{route.name}"


openapi_tags = [
    {
        "name": "admin",
        "description": "这部分API与管理员操作相关, 包括用户管理和权限控制等功能. ",
    },
]

app = FastAPI(
    # docs_url=None,
    # redoc_url=None,
    title=settings.PROJECT_NAME,
    description="mtmai description(group)",
    version=version,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={
        "syntaxHighlight": True,
        "syntaxHighlight.theme": "obsidian",
    },
    openapi_tags=openapi_tags,
)
templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):  # noqa: ARG001
    return JSONResponse(status_code=500, content={"detail": str(exc)})


app.include_router(home.router)
app.include_router(api_router, prefix=settings.API_V1_STR)


# 实验: 使用中间件的方式动态设置 cors
class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        response = await call_next(request)

        if origin and origin in settings.BACKEND_CORS_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Authorization, Content-Type, X-CSRF-Token"
        )

        return response


async def serve():
    import uvicorn

    if settings.OTEL_ENABLED:
        from mtmai.mtlibs import otel

        otel.setup_otel(app)

    app.add_middleware(DynamicCORSMiddleware)
    if settings.BACKEND_CORS_ORIGINS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            # allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    if (
        not settings.is_in_vercel
        and not settings.is_in_gitpod
        and settings.CF_TUNNEL_TOKEN
        and not coreutils.is_in_huggingface()
        and not coreutils.is_in_windows()
    ):
        from mtmlib import tunnel

        threading.Thread(target=tunnel.start_cloudflared).start()
    if not is_in_vercel() and not settings.is_in_gitpod:
        from mtmai.api.routes.search import run_searxng_server

        threading.Thread(target=run_searxng_server).start()

    if (
        not settings.is_in_vercel
        and not settings.is_in_gitpod
        and not coreutils.is_in_windows()
    ):
        from mtmai.api.serve.front import start_front_app

        threading.Thread(target=start_front_app).start()

    if (
        not is_in_vercel()
        and not settings.is_in_gitpod
        and not coreutils.is_in_windows()
    ):
        from mtmai.api.serve.vnc import start_vnc_server

        threading.Thread(target=start_vnc_server).start()

    if (
        not settings.is_in_vercel
        and not settings.is_in_gitpod
        and not coreutils.is_in_windows()
    ):
        from mtmai.api.serve.codeserver import start_code_server

        threading.Thread(target=start_code_server).start()

    logger.info("🚀 mtmaiapi serve on : %s:%s", settings.SERVE_IP, settings.PORT)
    config = uvicorn.Config(app, host=settings.SERVE_IP, port=settings.PORT)
    server = uvicorn.Server(config)
    await server.serve()


def main():
    parser = argparse.ArgumentParser(description="mtmai")
    parser.add_argument(
        "command",
        help="Specify the command to run, e.g., 'init' to run initialization.",
        nargs="?",
        default="serve",
    )

    args = parser.parse_args()
    if args.command == "init":
        from mtmai.mtlibs import dev_helper

        dev_helper.init_project()
        return

    elif args.command == "clean":
        from mtmai.mtlibs import dev_helper

        dev_helper.run_clean()
        return
    elif args.command == "test":
        from mtmai.mtlibs import dev_helper

        dev_helper.run_testing()
        return

    elif args.command == "release":
        from mtmai.mtlibs import dev_helper

        dev_helper.release_py()
        return

    elif args.command == "dp":
        from mtmai.mtlibs import dev_helper

        dev_helper.run_deploy()
        return

    elif args.command == "docker_build_base":
        from mtmai.mtlibs import dev_helper

        dev_helper.docker_build_base()
        return

    elif args.command == "release_npm":
        from mtmai.mtlibs import dev_helper

        dev_helper.release_npm()
        return

    elif args.command == "dp_cfpage":
        from mtmai.mtlibs import dev_helper

        dev_helper.dp_cfpage()
        return
    elif args.command == "gen":
        from mtmai.mtlibs import dev_helper

        dev_helper.gen()
        return

    elif args.command == "tunnel":
        from mtmlib import tunnel

        tunnel.start_cloudflared()
        return
    elif args.command == "serve":
        logger.info("🚀 call serve : %s:%s", settings.HOSTNAME, settings.PORT)
        asyncio.run(serve())
        return

    msg = f'unknown command: "{args.command}"'
    raise Exception(msg)  # noqa: TRY002


if __name__ == "__main__":
    main()
