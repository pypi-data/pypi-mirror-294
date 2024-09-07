from .accounts import AccountsCommands
from .auth import AuthCommands
from .base_commands import BaseCommands
from .cde import CdeCommands
from .config import ConfigCommands
from .pdd import PddCommands
from .tasks import TasksCommands
from .users import UsersCommands


class Commands(BaseCommands):
    accounts = AccountsCommands
    auth = AuthCommands
    cdeset = CdeCommands
    config = ConfigCommands
    pdd = PddCommands
    users = UsersCommands
    tasks = TasksCommands
