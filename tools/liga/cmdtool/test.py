from nameko.standalone.rpc import ClusterRpcProxy
import config

config = {
    'AMQP_URI': config.local_config['amqp_uri']
}

print(config)

with ClusterRpcProxy(config) as cluster_rpc:
    aux = cluster_rpc.batman_service.hello("renato")
    print(aux)