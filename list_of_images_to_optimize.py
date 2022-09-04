"""
The first element is the docker image name
the second element is optional and is the workload to optimize for.

If the workload is not specified, the default entrypoint and arguments
of the image are used.
"""


images_to_optimize = [
    # python images
    ["python:3.7", '["python", "-c", "print(\'hello world\')"]'],
    ["python:3.8", '["python", "-c", "print(\'hello world\')"]'],
    ["python:3.9", '["python", "-c", "print(\'hello world\')"]'],
    ["python:3.10", '["python", "-c", "print(\'hello world\')"]'],
    ["python:3.10-slim", '["python", "-c", "print(\'hello world\')"]'],

    # databases images
    ["postgres:14.2"],
    ["wordpress:5.9.2"],
    ["rabbitmq:3.9.14"],
]
