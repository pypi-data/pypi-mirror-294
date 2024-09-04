from . import set_hook
from .worker import init_hud_thread as init

set_hook()

__all__ = ["init"]
