# -*- coding: utf-8 -*-
import argparse
import os
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response

from database import init_db

app = FastAPI(
    title="API Agent"
)
# app.include_router(api.projects.router)



@app.on_event("startup")
async def startup_event():
    """
    Run before the application starts. Creates tables in the database.
    """
    init_db()


@app.get("/", response_class=PlainTextResponse)
async def ping():
    """
    Handles GET requests to /.
    """
    return "pong"


def enable_cors():
    """
    Enables CORS preflight requests.
    """

    @app.options("/{rest_of_path:path}")
    async def preflight_handler(request: Request, rest_of_path: str) -> Response:
        """
        Handles CORS preflight requests.
        """
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers[
            "Access-Control-Allow-Methods"
        ] = "POST, GET, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response

    @app.middleware("http")
    async def add_cors_header(request: Request, call_next):
        """
        Sets CORS headers.
        """
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers[
            "Access-Control-Allow-Methods"
        ] = "POST, GET, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response


if os.getenv("ENABLE_CORS"):
    enable_cors()


def parse_args(args):
    """Takes argv and parses API options."""
    parser = argparse.ArgumentParser(
        description="Project API",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for HTTP server (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP server (default: 8080)",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    uvicorn.run(app, host=args.host, port=args.port)
