from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client, docker_low_client
import docker, json
from capitan.blueprints.login_required import login_required

url_prefix = '/services'
bp = Blueprint('services', __name__)


@bp.route('/')
@login_required
def index():
    def compose_service(service):
        attributes = service.attrs
        return {
            'Id': service.id,
            'Name': service.name,
            'Image': attributes['Spec']['TaskTemplate']['ContainerSpec']['Image'],
            'Replicas': attributes['Spec']['Mode'].get('Replicated', {}).get('Replicas', 0)
        }

    services = [compose_service(s) for s in docker_client.services.list()]
    return render_template('services/index.html', services=services)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        ports = None
        if request.form['target_port'] and request.form['published_port']:
            ports = {}
            ports[int(request.form['target_port'])] = int(request.form['published_port'])

        options = {
            'command': [request.form['command']] if request.form['command'] else None,
            'args': [request.form['arguments']] if request.form['arguments'] else None,
            'name': request.form['name'],
            'endpoint_spec': docker.types.EndpointSpec(ports=ports),
            'mode': docker.types.ServiceMode('replicated', replicas=int(float(request.form['replicas'])))
        }

        if request.form['constraint']:
            options['constraints'] = request.form['constraint']

        docker_client.services.create(
          request.form['image'],
          **options
        )
        return redirect(url_for('.index'))

    return render_template('services/new.html')


@bp.route('/<path:service_id>', methods=['GET'])
@login_required
def show(service_id):
    services = docker_client.services.list(filters={'id': service_id})
    if not services:
        abort(404)
    service = services[0]

    log = b""
    for line in docker_low_client.service_logs(service.id, stdout=True, stderr=True, tail=100):
        log += line
    log = log.decode('utf-8')

    inspect = docker_low_client.inspect_service(service.id)
    inspect = json.dumps(inspect, sort_keys = False, indent = 2)

    tasks = docker_low_client.tasks(filters={'service': service.id })

    nodes = {t['ID']:docker_low_client.inspect_node(t['NodeID']) for t in tasks}

    return render_template('services/show.html', service=service, log=log, inspect=inspect, tasks=tasks, nodes=nodes)


@bp.route('/<path:service_id>', methods=['DELETE'])
@login_required
def delete(service_id):
    services = docker_client.services.list(filters={'id': service_id})

    if services:
        service = services[0]
        service.remove()
        return (f'Service {service_id} deleted!', 204)
    else:
        return ('Error', 404)
