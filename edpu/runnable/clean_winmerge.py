def main() -> None:
    from edpu.win_reg import reg_delete

    root = r'HKCU\Software\Thingamahoochie\WinMerge'

    reg_delete(fr'{root}\Editor')
    reg_delete(fr'{root}\Files')
    reg_delete(fr'{root}\Recent File List')


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
