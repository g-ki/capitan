from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
import docker

bp = Blueprint('capitan', __name__)
client = docker.from_env()

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

@bp.route('/status')
def status():
    status = docker.DockerClient(base_url='unix://var/run/docker.sock').info()

    base_status = [
        'Containers', 'ContainersRunning', 'ContainersPaused', 'ContainersStopped', 'Images',
        'DockerRootDir', 'Name', 'Driver'
    ]
    generated_status = { your_key: status[your_key] for your_key in base_status }
    generated_status['SwarmAddr'] = status['Swarm']['NodeAddr']
    return render_template('status.html', status=generated_status)

@bp.route('/containers')
def containers():
    client1 = docker.APIClient(base_url='unix://var/run/docker.sock')
    containers = client.containers.list();
    containers_ports = {}
    for container in containers:
        ports = client1.inspect_container(container.id)['NetworkSettings']['Ports']
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

@bp.route('/')
def dashboard():
    return "Dashboard ..."

@bp.route('/add-worker')
def add_worker():
    token = client.swarm.attrs['JoinTokens']['Worker']
    address = client.info()['Swarm']['RemoteManagers'][0]['Addr']
    script = f"docker swarm join --token {token} {address}"

    return render_template('add-worker.html', script=script)

@bp.route('/nodes')
def nodes():
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

    nodes = list(map(compose_node, client.nodes.list()))

    return render_template('nodes.html', nodes=nodes)

@bp.route('/services')
def services():
    def compose_service(service):
        attributes = service.attrs
        return {
            'Name': service.name,
            'Image': attributes['Spec']['TaskTemplate']['ContainerSpec']['Image'],
            'Replicas': attributes['Spec']['Mode'].get('Replicated', {}).get('Replicas', 0)
        }

    services = list(map(compose_service, client.services.list()))

    return render_template('services.html', services=services)

@bp.route('/add-serivce', methods=['GET', 'POST'])
def add_service():
      if request.method == 'POST':
          client.services.create(
            request.form['image'],
            command=[request.form['command']],
            args=[request.form['arguments']],
            name=request.form['name'],
            constraints=[request.form['constraint']],
            mode=docker.types.ServiceMode('replicated', replicas=int(float(request.form['replicas'])))
          )

          return redirect(url_for('capitan.services'))
      return render_template('add-service.html')



@bp.route('/404')
def page_not_found():
    current_app.logger.error('this is error')
    return render_template('page_not_found.html'), 404
