from .utils.data import DataProvider


def run(data_provider: DataProvider) -> None:
    from .. import pause_at_end
    from typing import Callable, Optional

    def init_state(bootstrap: Optional[bool], flip_bootstrap_mode: Optional[Callable[[], None]]) -> None:
        from .utils.actions import init_state as impl
        impl(data_provider, bootstrap, flip_bootstrap_mode)

    def main() -> None:
        from .utils.utils import Args
        args = Args.parse()

        if args is None:
            from .facades.pick import pick

            bootstrap_mode = False

            def flip_bootstrap_mode() -> None:
                nonlocal bootstrap_mode
                bootstrap_mode = not bootstrap_mode
                print('bootstrap_mode == ' + str(bootstrap_mode))

            init_state(None, flip_bootstrap_mode)
            pick(lambda: bootstrap_mode, data_provider.get_filename(), data_provider.is_debug())

        else:
            from .facades.run import run

            init_state(args.bootstrap, None)
            run(args.action, args.bootstrap)

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
