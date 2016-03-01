# Logspout

Ship your app-container logs to Logstash!

## Usage

This charm relates to any other charm that implements the `dockerhost` interface.
Its a subordinate relation, which means that logspout will attach to the host
and launch a container, bind-mounting the docker socket into the container so it
can process and ship log events to a remote source, such as logstash!

## Deployment

     juju deploy ~lazypower/bundle/logstash-core
     juju deploy trusty/docker
     juju deploy trusty/logspout
     juju add-relation logspout docker
     juju add-relation logspout logstash

You can test that the entire logging pipeine is working by invoking the
`generate-logspam` action on one of the logspout hosts

     juju action do logspout/0 generate-logspam

You can then visit the kibana interface to see your log messages successfully
shipped from the docker host, though an intermediary logstash logrouting
service, archived in elasticsearch, and finally - visualized for you in kibana

    juju expose kibana
    juju status kibana
    open http://`public-address`

## Maintainers

 - Charles Butler &lt;charles.butler@canonical.com&gt;
 - Matt Bruzek &lt;matthew.bruzek@canonical.com&gt;
