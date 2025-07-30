def run(items: list[str]) -> None:
    from .button_window import run, ButtonDefs


    def button_defs() -> ButtonDefs:
        result: ButtonDefs = []

        for item in items:
            from .button_window import ButtonCommand

            def command() -> ButtonCommand:
                item_copy = item

                def impl() -> None:
                    from pyperclip import copy
                    copy(item_copy)

                return impl

            result.append((item, command()))

        return result


    run(button_defs(), 'clipboard_copier')
