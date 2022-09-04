import subprocess
from list_of_images_to_optimize import images_to_optimize

CONVERTED_IMAGES_PREFIX = "docker.io/gabrieldemarmiesse/"
COMPRESSION_LEVEL = 6


def create_and_push_org_image(docker_image_name: str):
    copy_of_original_docker_image = CONVERTED_IMAGES_PREFIX + docker_image_name + "org"

    subprocess.check_call(["nerdctl", "tag", docker_image_name, copy_of_original_docker_image])
    subprocess.check_call(["nerdctl", "push", copy_of_original_docker_image])


def create_and_push_esgz_image(docker_image_name: str, entrypoint):
    if "/" not in docker_image_name:
        normalized_docker_image_name = "docker.io/library/" + docker_image_name
    else:
        normalized_docker_image_name = docker_image_name
    estargz_docker_image_name = CONVERTED_IMAGES_PREFIX + docker_image_name + "esgz"

    if entrypoint:
        additional_options = ["--entrypoint", entrypoint]
    else:
        additional_options = []
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


def convert_and_push(docker_image_name: str, entrypoint=None):
    subprocess.check_call(["nerdctl", "pull", docker_image_name])

    create_and_push_org_image(docker_image_name)
    create_and_push_esgz_image(docker_image_name, entrypoint)


for image_and_args in images_to_optimize:
    convert_and_push(*image_and_args)
