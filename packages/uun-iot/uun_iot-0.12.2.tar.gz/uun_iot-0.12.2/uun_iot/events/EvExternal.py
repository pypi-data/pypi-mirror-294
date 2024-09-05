import logging
import typing as t
from dataclasses import dataclass

from ..exceptions import EventCannotRegisterHandler
from ..utils import classproperty
from .Event import Event, EventType, Register

logger = logging.getLogger(__name__)

SelfM = t.Any
F = t.TypeVar("F")


class DuplicateKeyError(ValueError):
    pass


K = t.TypeVar("K")
V = t.TypeVar("V")


@dataclass
class DuplicateKeyErrStruct(t.Generic[K, V]):
    key: K
    current: V
    new: V


def dict_throw_on_duplicate_keys(
    it: t.Iterable[t.Tuple[K, V]],
) -> t.Dict[K, V]:
    d = {}
    for k, v in it:
        if k in d:
            raise DuplicateKeyError(DuplicateKeyErrStruct(k, d[k], v))
        d[k] = v
    return d


def dict_append_on_duplicate_keys(
    it: t.Iterable[t.Tuple[K, V]],
) -> t.Dict[K, t.List[V]]:
    d = {}
    for k, v in it:
        if k not in d:
            d[k] = [v]
        else:
            d[k].append(v)
    return d


def populate_handlers(
    it: t.Iterable[t.Tuple[K, V]], fn: t.Callable[[DuplicateKeyErrStruct], str]
) -> t.Dict[K, V]:
    try:
        return dict_throw_on_duplicate_keys(it)
    except DuplicateKeyError as e:
        einfo = e.args[0]
        raise ValueError(fn(einfo)) from e


class EvExternal(Event):
    """
    Event for mediating socket commands. This class acts as an intermediary between the
    socket server and handlers. See :class:`uun_iot.modules.ConfUpdater` for more
    details.

    Examples:

        - configuration:

            .. code-block:: json

                {
                    "gateway": {
                        "socket": {
                            "path-to-socket-file.socket"
                        }
                    }
                }

        .. code-block:: python

            from uun_iot import EvExternal

            class ExternallyControlledModule:
                @EvExternal.subscribe_command("action1")
                def handle_cmd(self, msg):
                    cmd, msg = msg
                    assert(cmd == "action1")
                    print(msg)

            >>> echo "action1 This message was created outside of the main Python app." | nc -U path/to/unix/socket.sock
            >>> # handle_cmd is called and prints
            >>> 'This message was created outside of the main Python app.'
    """

    event_type = EventType.EXTERNAL
    _handlers: t.Dict[str, t.Callable]

    def __init__(self, config=None):
        self._handlers = {}
        super().__init__(config=None)

    @classmethod
    def subscribe_command(cls, action_id: str):
        """Subscribe to socket command.

        The handler is passed positional argument ``msg`` as a tuple ``(cmd, rest_msg)``,
        where cmd is the issued command and ``rest_msg`` is the rest of the
        message received by socket IPC

        Args:
            action_id: string identifier of action
        """
        if not isinstance(action_id, str):
            raise EventCannotRegisterHandler("Only string action IDs are supported.")
        return cls._register(
            Register[
                t.Callable[[SelfM, t.Tuple[str, t.Optional[str]]], t.Optional[str]]
            ],
            action_id,
        )

    def add_handlers(self, handler_list):
        # self._handlers = {info.args[0]: fn for fn, info in handler_list}
        self._handlers = populate_handlers(
            ((info.args[0], fn) for fn, info in handler_list),
            lambda einfo: f"Encountered duplicate entry for @EvExternal.handle_action, id '{einfo.key}'",
        )

    def get_handler(
        self, action_id: str
    ) -> t.Optional[t.Callable[[t.Tuple[str, t.Optional[str]]], t.Optional[str]]]:
        """Get handler with action_id, if exists.

        Args:
            action_id: identifier of handler
        """
        return self._handlers.get(action_id)

    def start(self):
        """Noop"""
        pass

    def stop(self):
        """Noop"""
        pass
