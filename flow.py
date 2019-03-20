from kubernetes import client, config
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
    pods = core.list_namespaced_pod(watch=False, namespace=ns,
                                    label_selector=f'app={label}')
    for p in pods.items:
        return p


def getContainerImage():
    p = getPod(app)
    # TO-DO create filter for sidecar exclude
    for c in p.spec.containers:
        return c.image


def checkImageUpdate():
    i = getContainerImage()
    local_image_id = docker_client.images.get(i).id
    pulled_image_id = docker_client.images.pull(i, tag='latest').id
    if local_image_id == pulled_image_id:
        print(f'No changes for {i}')
    else:
        deletePod()
        print(f'{i} have changes. New pod is created.')


def deletePod():
    p = getPod(app)
    return core.delete_namespaced_pod(p.metadata.name, ns,
                                      body=client.V1DeleteOptions())


def run():
    while True:
        time.sleep(20)
        checkImageUpdate()


if __name__ == '__main__':
    run()
