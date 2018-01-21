from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from capitan.app import docker_client, docker_low_client

bp = Blueprint('capitan', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #
        # TODO:
        # validate and login ..
        #
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('capitan.status'))
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('capitan.login'))


@bp.route('/')
def index():
    status = docker_client.info()

    base_status = [
        'Containers', 'ContainersRunning', 'ContainersPaused', 'ContainersStopped', 'Images',
        'DockerRootDir', 'Name', 'Driver'
    ]
    generated_status = { your_key: status[your_key] for your_key in base_status }
    generated_status['SwarmAddr'] = status['Swarm']['NodeAddr']
    return render_template('status.html', status=generated_status)


@bp.route('/containers')
def containers():
    containers = docker_client.containers.list();
    containers_ports = {}
    for container in containers:
        ports = docker_low_client.inspect_container(container.id)['NetworkSettings']['Ports']
        container_ports = []
        for inside_port, outside_port in ports.items():
            if outside_port:
                host_ip = outside_port[0]['HostIp']
                host_port = outside_port[0]['HostPort']
                container_ports.append(f"{inside_port} -> {host_ip}:{host_port}")
            else:
                container_ports.append(f"{inside_port}")
        containers_ports[container.id] = ', '.join(container_ports)
    return render_template('containers.html', containers=containers, ports=containers_ports)
