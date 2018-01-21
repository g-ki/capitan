from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client
import docker

url_prefix = '/services'
bp = Blueprint('services', __name__)


@bp.route('/')
def index():
    def compose_service(service):
        attributes = service.attrs
        return {
            'Name': service.name,
            'Image': attributes['Spec']['TaskTemplate']['ContainerSpec']['Image'],
            'Replicas': attributes['Spec']['Mode'].get('Replicated', {}).get('Replicas', 0)
        }

    services = [compose_service(s) for s in docker_client.services.list()]
    return render_template('services/index.html', services=services)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        docker_client.services.create(
          request.form['image'],
          command=[request.form['command']],
          args=[request.form['arguments']],
          name=request.form['name'],
          constraints=[request.form['constraint']],
          mode=docker.types.ServiceMode('replicated', replicas=int(float(request.form['replicas'])))
        )
        return redirect(url_for('.new'))

    return render_template('services/new.html')


@bp.route('/<path:service_id>')
def user(service_id):
    return f"Service with {service_id}"
