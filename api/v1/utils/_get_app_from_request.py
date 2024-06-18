from fastapi import Request

from app import AppInterface


def get_app_from_request(request: Request) -> AppInterface:
    return request.app.app
