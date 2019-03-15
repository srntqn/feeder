from kubernetes import client, config
import docker
import time
import os

config.load_incluster_config()  # for execution inside k8s cluster
# config.load_kube_config()  # for local execution
app = os.environ['app']
core = client.CoreV1Api()
apps = client.AppsV1Api()
docker_client = docker.from_env()


def getPod(pod):
    pods = core.list_namespaced_pod(watch=False, namespace='default',
                                    label_selector=f'app={pod}')
    for p in pods.items:
        return p


def getContainerImage(pod):
    p = getPod(pod)
    for c in p.spec.containers:
        return c.image


def checkImageUpdate():
    i = getContainerImage(app)
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
