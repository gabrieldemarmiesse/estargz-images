import subprocess
from concurrent.futures import ThreadPoolExecutor

from list_of_images_to_optimize import Image, images_to_optimize

CONVERTED_IMAGES_PREFIX = "docker.io/gabrieldemarmiesse/estargz-images"


def get_normalized_image_name(docker_image_name: str) -> str:
    """We add docker.io/library/ if necessary"""
    if "/" not in docker_image_name:
        return "docker.io/library/" + docker_image_name
    else:
        return docker_image_name


class ConversionJob:
    def __init__(self, src_image: Image):
        self.src_image = src_image

    def ctr_remote_image_optimize(
        self, optimize: bool = True, zstdchunked: bool = False
    ):
        src_image_name = get_normalized_image_name(self.src_image.name)

        additional_options = []
        if self.src_image.entrypoint is not None:
            additional_options += ["--entrypoint", self.src_image.entrypoint]
        if not optimize:
            additional_options.append("--no-optimize")
        if zstdchunked:
            additional_options.append("--zstdchunked")

        subprocess.check_call(
            [
                "ctr-remote",
                "image",
                "optimize",
                "--oci",
                "--no-optimize",
                src_image_name,
                self.converted_image_name,
            ]
            + additional_options
        )

    @property
    def converted_image_name(self) -> str:
        raise NotImplementedError("You need to subclass and implement this method")

    def convert(self):
        raise NotImplementedError("You need to subclass and implement this method")

    def push(self):
        """Can be overwritten for the carbon copy (no-op, crane already copy it)"""
        subprocess.check_call(["nerdctl", "push", self.converted_image_name])

    def job_was_already_done(self) -> bool:
        """We check if the docker image already exists"""
        try:
            subprocess.check_call(["crane", "digest", self.converted_image_name])
            return True
        except subprocess.CalledProcessError:
            return False

    def pull_convert_and_push(self):
        if self.job_was_already_done():
            print(f"--> Image {self.converted_image_name} is already in the registry")
            return
        subprocess.check_call(["nerdctl", "pull", self.src_image.name])
        self.convert()
        self.push()
        print(f"--> Pushed {self.converted_image_name} to registry")


class OriginalConversionJob(ConversionJob):
    @property
    def converted_image_name(self) -> str:
        return f"{CONVERTED_IMAGES_PREFIX}/{self.src_image.name}-org"

    def convert(self):
        subprocess.check_call(
            [
                "crane",
                "copy",
                "--platform",
                "linux/amd64",
                self.src_image.name,
                self.converted_image_name,
            ]
        )

    def push(self):
        pass


class StargzConversionJob(ConversionJob):
    @property
    def converted_image_name(self) -> str:
        return f"{CONVERTED_IMAGES_PREFIX}/{self.src_image.name}-esgz-noopt"

    def convert(self):
        self.ctr_remote_image_optimize(optimize=False)


class EStargzConversionJob(ConversionJob):
    @property
    def converted_image_name(self) -> str:
        return f"{CONVERTED_IMAGES_PREFIX}/{self.src_image.name}-esgz"

    def convert(self):
        self.ctr_remote_image_optimize()


class EStargzZstdchunkedConversionJob(ConversionJob):
    @property
    def converted_image_name(self) -> str:
        return f"{CONVERTED_IMAGES_PREFIX}/{self.src_image.name}-zstdchunked"

    def convert(self):
        self.ctr_remote_image_optimize(zstdchunked=True)


def main():
    conversion_jobs = []

    for image_and_args in images_to_optimize:
        conversion_jobs += [
            OriginalConversionJob(image_and_args),
            StargzConversionJob(image_and_args),
            EStargzConversionJob(image_and_args),
            EStargzZstdchunkedConversionJob(image_and_args),
        ]

    # 3 threads for more speed
    with ThreadPoolExecutor(max_workers=3) as pool:
        pool.map(ConversionJob.pull_convert_and_push, conversion_jobs)
    print("--> All done!")


if __name__ == "__main__":
    main()
