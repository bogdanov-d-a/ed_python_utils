from __future__ import annotations
from .data import DataProvider
from typing import Callable, Optional


class Action:
    def __init__(self: Action, cmd: str, name: str, handler: Callable[[], None], in_place: bool) -> None:
        self.cmd = cmd
        self.name = name
        self.handler = handler
        self.in_place = in_place


Actions = list[Action]


class State:
    def __init__(self: State, data_provider: DataProvider, bootstrap: Optional[bool], flip_bootstrap_mode: Optional[Callable[[], None]], quit: Optional[Callable[[], None]]) -> None:
        self.data_provider = data_provider
        self.bootstrap = bootstrap
        self.flip_bootstrap_mode = flip_bootstrap_mode
        self.quit = quit

    def get_bootstrap(self: State) -> bool:
        if self.bootstrap is None:
            raise Exception()
        return self.bootstrap

    def get_flip_bootstrap_mode(self: State) -> Callable[[], None]:
        if self.flip_bootstrap_mode is None:
            raise Exception()
        return self.flip_bootstrap_mode

    def get_quit(self: State) -> Callable[[], None]:
        if self.quit is None:
            raise Exception()
        return self.quit


def init_state(data_provider: DataProvider, bootstrap: Optional[bool], flip_bootstrap_mode: Optional[Callable[[], None]], quit: Optional[Callable[[], None]]) -> None:
    global state
    state = State(data_provider, bootstrap, flip_bootstrap_mode, quit)


def get_state() -> State:
    return state


def all() -> Actions:
    from ..impl import impl
    from ..impl.create_bundle import create_bundle
    from ..impl.user_bundle.apply import apply_user_bundle
    from ..impl.user_bundle.create import create_user_bundle
    from ..impl.user_bundle.get_info import get_user_bundle_info

    bootstrap_mode_filter = lambda: get_state().data_provider.get_bootstrap_repos() if get_state().get_bootstrap() else None

    def host_repos_push_native() -> None:
        filter_ = get_state().data_provider.get_autopush_repos()

        if get_state().get_bootstrap():
            filter_ &= get_state().data_provider.get_bootstrap_repos()

        impl.host_repos_push_native(get_state().data_provider.get_repos(), filter_)

    return [
        Action(
            's',
            'Status',
            lambda: impl.host_repos_status(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'lref',
            'List refs',
            lambda: impl.host_repos_all_refs(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'lrefs',
            'List storage refs',
            lambda: impl.host_repos_all_storage_refs(
                get_state().data_provider.get_repos(),
                get_state().data_provider.get_storage_block_reasons(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'lrem',
            'List remotes',
            lambda: impl.host_repos_remotes(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'lst',
            'List stash',
            lambda: impl.host_repos_all_stash(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'fen',
            'Fetch native',
            lambda: impl.host_repos_fetch(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'fes',
            'Fetch storage',
            lambda: impl.host_repos_fetch_storage(
                get_state().data_provider.get_repos(),
                get_state().data_provider.get_storage_block_reasons(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'pln',
            'Pull native',
            lambda: impl.host_repos_pull_native(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'pls',
            'Pull storage',
            lambda: impl.host_repos_pull_storage(
                get_state().data_provider.get_repos(),
                get_state().data_provider.get_storage_block_reasons(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'psn',
            'Push native',
            host_repos_push_native,
            False
        ),
        Action(
            'pss',
            'Push storage',
            lambda: impl.host_repos_push_storage(
                get_state().data_provider.get_repos(),
                get_state().data_provider.get_storage_block_reasons(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'fsck',
            'Run fsck',
            lambda: impl.host_repos_fsck(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'fscks',
            'Run fsck storage',
            lambda: impl.host_repos_fsck_storage(
                get_state().data_provider.get_repos(),
                get_state().data_provider.get_storage_block_reasons(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'gc',
            'Run gc',
            lambda: impl.host_repos_gc(get_state().data_provider.get_repos(), bootstrap_mode_filter()),
            False
        ),
        Action(
            'bc',
            'Create bundle',
            lambda: create_bundle(
                get_state().data_provider.get_bundle_hash_path,
                get_state().data_provider.get_bundle_path(),
                get_state().data_provider.get_bundle_block_reasons(),
                get_state().data_provider.get_repos(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'bui',
            'Get user bundle info',
            lambda: get_user_bundle_info(
                get_state().data_provider.get_user_bundle_info_path(),
                get_state().data_provider.get_repos(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'buc',
            'Create user bundle',
            lambda: create_user_bundle(
                get_state().data_provider.get_user_bundle_info_new_path(),
                get_state().data_provider.get_bundle_path(),
                get_state().data_provider.get_repos(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'bua',
            'Apply user bundle',
            lambda: apply_user_bundle(
                get_state().data_provider.get_bundle_path(),
                get_state().data_provider.get_repos(),
                bootstrap_mode_filter()
            ),
            False
        ),
        Action(
            'fbm',
            'Flip bootstrap_mode',
            lambda: get_state().get_flip_bootstrap_mode()(),
            True
        ),
        Action(
            'q',
            'Quit',
            lambda: get_state().get_quit()(),
            True
        ),
    ]


def find_by_cmd(cmd: str) -> Action:
    for action in all():
        if action.cmd == cmd:
            return action

    raise Exception('unexpected action ' + cmd)
