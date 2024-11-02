def main() -> None:
    from edpu.win_reg import reg_delete
    reg_delete(r'HKCU\Software\7-Zip')


if __name__ == '__main__':
    from edpu import pause_at_end
    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
