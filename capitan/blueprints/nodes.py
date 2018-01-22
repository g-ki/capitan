import time
from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client
import digitalocean

url_prefix = '/nodes'
bp = Blueprint('nodes', __name__)


@bp.route('/')
def index():
    def compose_node(node):
        attributes = node.attrs
        return {
            'Host': attributes['Description']['Hostname'],
            'Id': attributes['ID'],
            'Role': attributes['Spec']['Role'],
            'EngineVersion': attributes['Description']['Engine']['EngineVersion'],
            'State': attributes['Status']['State'],
            'Addr': attributes['Status']['Addr'],
            'ManagerAddr': attributes.get('ManagerStatus', {}).get('Addr', '-')
        }

    nodes = list(map(compose_node, docker_client.nodes.list()))

    return render_template('nodes/index.html', nodes=nodes)


@bp.route('/new')
def new():
    token = docker_client.swarm.attrs['JoinTokens']['Worker']
    address = docker_client.info()['Swarm']['RemoteManagers'][0]['Addr']
    script = f"docker swarm join --token {token} {address}"

    if 'DOCEAN_TOKEN' in current_app.config:
        time_id = int(time.time())
        droplet = digitalocean.Droplet(
            token=current_app.config['DOCEAN_TOKEN'],
            name=f'worker-{time_id}',
            region='fra1', # Frankfurt 1
            image='ubuntu-16-04-x64', # Ubuntu 16.04 x64
            size_slug='s-1vcpu-1gb',  # 1vcpu + 1gb
            ssh_keys=[], # TODO: use ssh keys
            user_data=None # TODO: write cloud-init script
        )
        # droplet.create()

    return render_template('nodes/new.html', script=script)


@bp.route('/<path:node_id>')
def show(node_id):
    return f"Node {node_id}"
