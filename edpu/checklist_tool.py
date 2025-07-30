from __future__ import annotations
from typing import Callable


VoidFn = Callable[[], None]
BoolFn = Callable[[bool], None]


def show_checklist(items: list[str], title: str) -> None:
    from .tkinter_utils import non_resizable, center_window
    from tkinter import Tk, StringVar


    root = Tk()
    root.title(title)
    non_resizable(root)

    total_count = len(items)
    checked_count = 0


    def add_label() -> StringVar:
        variable = StringVar(root)

        from tkinter.ttk import Label
        Label(root, textvariable=variable).grid(row=0)

        return variable


    def make_label_updater(variable: StringVar) -> VoidFn:
        def impl() -> None:
            variable.set(f'{title} : {checked_count} / {total_count - checked_count} ({total_count})')

        impl()
        return impl


    def make_stat_updater(label_updater: VoidFn) -> BoolFn:
        def impl(checked: bool) -> None:
            nonlocal checked_count

            if checked:
                checked_count += 1
            else:
                checked_count -= 1

            label_updater()

        return impl


    def add_checkbuttons(stat_updater: BoolFn) -> None:
        for item, index in zip(items, range(total_count)):
            def impl() -> None:
                from tkinter import IntVar, W
                from tkinter.ttk import Checkbutton

                variable = IntVar(root)

                Checkbutton(
                    root,
                    text=item,
                    variable=variable,
                    command=lambda: stat_updater(variable.get() != 0)
                ).grid(row=index + 1, sticky=W)

            impl()


    add_checkbuttons(
        make_stat_updater(
            make_label_updater(
                add_label()
            )
        )
    )


    center_window(root)
    root.mainloop()


def show_picker(checklists: list[tuple[str, list[str]]]) -> None:
    from .button_window import run, ButtonDefs


    def button_defs() -> ButtonDefs:
        result: ButtonDefs = []

        for name, items in checklists:
            from .button_window import ButtonCommand

            def command() -> ButtonCommand:
                name_copy = name
                items_copy = items

                def impl() -> bool:
                    show_checklist(items_copy, name_copy)
                    return False

                return impl

            result.append((name, command()))

        return result


    run(button_defs(), 'Checklists')
