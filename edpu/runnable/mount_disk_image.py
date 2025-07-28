if __name__ == '__main__':
    from edpu import pause_at_end
    from edpu.mount_disk_image import run_interactive
    pause_at_end.run(run_interactive, pause_at_end.DEFAULT_MESSAGE)
