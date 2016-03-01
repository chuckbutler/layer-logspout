from charms.reactive import when
from charms.reactive import set_state
from charms.reactive import remove_state

from charms.docker import Docker
from charms.docker.compose import Compose

from charmhelpers.core.hookenv import config
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.templating import render


@when('docker.available')
def logspout_to_the_rescue():
    status_set('maintenance', 'Pulling logspout container image')
    d = Docker()
    d.pull(config('container-image'))
    set_state('logstash.pulled')
    status_set('waiting', 'Logspout image pulled')


@when('logstash.available')
def configure_logspout(logstash):
    remove_state('logstash.running')
    status_set('maintenance', 'Writing logspout config')
    src = 'docker-compose.yaml'
    tgt = 'files/logspout/docker-compose.yaml'
    context = {'private_address': logstash.private_address(),
               'udp_port': logstash.udp_port(),
               'container_image': config('container-image')}
    render(src, tgt, context)
    remove_state('logstash.available')
    set_state('logspout.ready')


@when('logspout.ready', 'logstash.pulled')
def start_logspout():
    compose = Compose('files/logspout')
    compose.up()
    remove_state('logspout.ready')
    status_set('active', 'Logspout running')
