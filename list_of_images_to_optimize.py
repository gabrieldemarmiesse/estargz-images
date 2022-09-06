"""
The first element is the docker image name
the second element is optional and is the workload to optimize for.

If the workload is not specified, the default entrypoint and arguments
of the image are used.
"""
from __future__ import annotations

from typing import Optional


class Image:
    def __init__(
        self,
        name: str,
        entrypoint: Optional[str] = None,
        env: dict = {},
        mount: list[tuple[str, str]] = [],
    ):
        self.name = name
        self.entrypoint = entrypoint
        self.env = env
        self.mount = mount


images_to_optimize = [
    # python images
    Image("python:3.7", '["python", "-c", "print(\'hello world\')"]'),
    Image("python:3.8", '["python", "-c", "print(\'hello world\')"]'),
    Image("python:3.9", '["python", "-c", "print(\'hello world\')"]'),
    Image("python:3.10", '["python", "-c", "print(\'hello world\')"]'),
    Image("python:3.10-slim", '["python", "-c", "print(\'hello world\')"]'),
    # databases images
    Image("postgres:14.2"),
    Image("wordpress:5.9.2"),
    Image("rabbitmq:3.9.14"),
]
