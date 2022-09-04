# estargz-images
A repository to convert existing Docker image to the estargz format

At every commit on master, the Docker images will be converted to the estargz format and pushed 
to the gabrieldemarmiesse/ namespace. You can then use those estargz images like so

```bash
nerdctl --snapshotter=stargz run -it gabrieldemarmiesse/python:3.9
```

If you want to add a docker image to the list of Docker images available for conversion, 
please make a pull request to add the public image here:

https://github.com/gabrieldemarmiesse/estargz-images/blob/master/list_of_images_to_optimize.py