import subprocess

CONVERTED_IMAGES_PREFIX = "docker.io/gabrieldemarmiesse/"
COMPRESSION_LEVEL = 6


def convert_and_push_one_image(docker_image_name: str):
    subprocess.check_call(["nerdctl", "pull", docker_image_name])

    if "/" not in docker_image_name:
        normalized_docker_image_name = "docker.io/library/" + docker_image_name
    else:
        normalized_docker_image_name = docker_image_name

    estargz_docker_image_name = CONVERTED_IMAGES_PREFIX + docker_image_name
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
    )
    subprocess.check_call(["nerdctl", "push", estargz_docker_image_name])
    return estargz_docker_image_name


convert_and_push_one_image("python:3.7")
