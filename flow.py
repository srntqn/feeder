from kubernetes import client, config
from kubernetes.client.rest import ApiException
import docker
import time
import os

config.load_incluster_config()  # for execution inside k8s cluster
# config.load_kube_config()  # for local execution
app = os.environ['app']
ns = 'default'

core = client.CoreV1Api()
apps = client.AppsV1Api()
docker_client = docker.from_env()


def getPod(label):
    try:
        pods = core.list_namespaced_pod(watch=False, namespace=ns,
                                        label_selector=f'app={label}')
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
    for p in pods.items:
        return p


def getContainerImage():
    p = getPod(app)
    # TO-DO create filter for sidecar exclude
    for c in p.spec.containers:
        return c.image


def getCurrentImageId():
    p = getPod(app)
    for i in p.status.container_statuses:
        print(i.image_id)


def deletePod():
    p = getPod(app)
    try:
        core.delete_namespaced_pod(p.metadata.name, ns,
                                   body=client.V1DeleteOptions())
    except ApiException as e:
        print(f"Exception when calling CoreV1Api->delete_namespaced_pod: {e}")


def checkImageUpdate():
    i = getContainerImage()
    local_image_id = docker_client.images.get(i).id
    pulled_image_id = docker_client.images.pull(i, tag='latest').id
    if local_image_id == pulled_image_id:
        print(f'No changes for {i}')
    else:
        deletePod()
        print(f'{i} have changes. New pod is created.')


def run():
    while True:
        time.sleep(20)
        checkImageUpdate()


if __name__ == '__main__':
    run()
