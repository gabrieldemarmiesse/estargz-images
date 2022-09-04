import subprocess

CONVERTED_IMAGES_PREFIX = "docker.io/gabrieldemarmiesse/"
COMPRESSION_LEVEL = 6


def convert_and_push(docker_image_name: str, entrypoint=None, args=None):
    subprocess.check_call(["nerdctl", "pull", docker_image_name])

    if "/" not in docker_image_name:
        normalized_docker_image_name = "docker.io/library/" + docker_image_name
    else:
        normalized_docker_image_name = docker_image_name

    estargz_docker_image_name = CONVERTED_IMAGES_PREFIX + docker_image_name

    additional_options = []
    if entrypoint:
        additional_options += ["--entrypoint", entrypoint]
    if args:
        additional_options += ["--args", args]
    subprocess.check_call(
        [
            "ctr-remote",
            "image",
            "optimize",
            "--oci",
            "--estargz-compression-level",
            str(COMPRESSION_LEVEL),
            normalized_docker_image_name,
            estargz_docker_image_name,
        ]
        + additional_options
    )
    subprocess.check_call(["nerdctl", "push", estargz_docker_image_name])
    subprocess.check_call(
        ["nerdctl", "image", "rm", docker_image_name, estargz_docker_image_name]
    )
    return estargz_docker_image_name


convert_and_push("python:3.7", entrypoint='["python", "-c", "print(\'hello world\')"]')
convert_and_push("python:3.8", entrypoint='["python", "-c", "print(\'hello world\')"]')
convert_and_push("python:3.9", entrypoint='["python", "-c", "print(\'hello world\')"]')
convert_and_push("python:3.10", entrypoint='["python", "-c", "print(\'hello world\')"]')
convert_and_push(
    "python:3.10-slim", entrypoint='["python", "-c", "print(\'hello world\')"]'
)
