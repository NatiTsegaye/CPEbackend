from Main.api.processApi import Process

def initialize_routes(api):
    api.add_resource(Process,'/process/')