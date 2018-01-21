from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client

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

    return render_template('nodes/new.html', script=script)


@bp.route('/<path:node_id>')
def show(node_id):
    return f"Node {node_id}"
