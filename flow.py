from kubernetes import client, config
import docker
import time

config.load_incluster_config()
v1 = client.CoreV1Api()
docker_client = docker.from_env()


def getContainerImage():
    pods = v1.list_namespaced_pod(watch=False, namespace='default')
    images = []
    for p in pods.items:
        for c in p.spec.containers:
            images.append(c.image)
    return images


def checkImageUpdate():
    for i in getContainerImage():
        local_image_id = docker_client.images.get(i).id
        pulled_image_id = docker_client.images.pull(i, tag='latest').id
        if local_image_id == pulled_image_id:
            print(f'No changes for {i}')
        else:
            print(f'Image {i} changed')


def run():
    while True:
        time.sleep(20)
        checkImageUpdate()


if __name__ == '__main__':
    run()
