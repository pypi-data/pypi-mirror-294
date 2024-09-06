from . import email  # noqa: F403
from . import logic  # noqa: F403
from .action import ai  # noqa: F403
from .action import arithmetic  # noqa: F403
from .action import format  # noqa: F403
from .action.ai import *  # noqa: F403
from .action.arithmetic import *  # noqa: F403
from .action.format import *  # noqa: F403
from .email import *  # noqa: F403
from .flow import Flow  # noqa: F401
from .logic import *  # noqa: F403
from .node import Node  # noqa: F401
from .source import constant  # noqa: F403
from .source.constant import *  # noqa: F403

GROUPS = [
    ("Email", email),
    ("AI", ai),
    ("Format", format),
    ("Constant Value", constant),
    ("Logic", logic),
    ("Maths", arithmetic),
]

MAP = {}
for group_name, module in GROUPS:
    for kls_name in module.__all__:
        kls = getattr(module, kls_name)
        MAP[kls_name] = (kls, kls.InitSchema, group_name)


def create_node(**json_payload):
    node_kls = json_payload.pop("kls")
    return MAP[node_kls][0].parse(**json_payload)
