from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client
import docker
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
        options = {
            'command': [request.form['command']],
            'args': [request.form['arguments']],
            'name': request.form['name'],
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


@bp.route('/<path:service_id>', methods=['DELETE'])
@login_required
def delete(service_id):
    services = docker_client.services.list(filters={'id': service_id})

    if services:
        service = services[0]
        service.remove()
        return (f'Node {service_id} deleted!', 204)
    else:
        return ('Error', 404)
