import json

import jsonpickle


def to_string(command_stack):
    dumps = json.dumps(json.loads(jsonpickle.encode(command_stack, unpicklable=True,keys=True)), indent=2)
    return dumps