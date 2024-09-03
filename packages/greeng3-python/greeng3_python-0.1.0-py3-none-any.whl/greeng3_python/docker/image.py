"""
docker run -it --rm \
   -v /var/run/docker.sock:/var/run/docker.sock \
   -v /usr/bin/docker:/usr/bin/docker \
   image:tag
"""

import docker


def pull_docker_image(image_name, tag='latest'):
    """
    Pulls a Docker image with the specified name and tag.
    Shows the build steps (layers) of the image.

    :param image_name: Name of the Docker image (e.g., 'ubuntu').
    :param tag: Tag of the Docker image (e.g., '20.04'). Defaults to 'latest'.
    """
    # Initialize Docker client
    client = docker.from_env()

    # Pull the Docker image
    print(f"Pulling Docker image: {image_name}:{tag}")
    try:
        image = client.images.pull(image_name, tag=tag)
        print(f"Successfully pulled image: {image_name}:{tag}\n")
    except docker.errors.APIError as e:
        print(f"Error pulling image {image_name}:{tag}: {e}")
        return

    # Display the image layers
    print(f"Build steps (layers) for image {image_name}:{tag}:")

    # Inspect image to retrieve its details
    image_info = client.images.get(f"{image_name}:{tag}").attrs

    # Extract the image layers
    if 'RootFS' in image_info and 'Layers' in image_info['RootFS']:
        layers = image_info['RootFS']['Layers']
        for idx, layer in enumerate(layers, start=1):
            print(f"Step {idx}: {layer}")
    else:
        print("No layers found for this image. It might be a minimal base image or there was an error.")


if __name__ == '__main__':
    # Example usage: replace 'ubuntu' and '20.04' with desired image and tag
    print("Enter")
    pull_docker_image('ubuntu', '20.04')
    print("Exit")
