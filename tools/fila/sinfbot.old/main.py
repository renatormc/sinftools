from nameko.rpc import rpc

class SinfbotService:
    name = "sinfbot"

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)