from nameko.standalone.rpc import ServiceRpcProxy

rpc_proxy = ServiceRpcProxy("sinfbot", {"AMQP_URI":"amqp://sinf:sptcICLR.@10.129.3.14:5672/sinf"}, timeout=5)

results = []
with rpc_proxy as proxy:
    res = proxy.hello("asdfsdaf")
    print(res)