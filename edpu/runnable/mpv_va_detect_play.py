if __name__ == '__main__':
    from edpu.mpv import mpv_va_detect_play
    from edpu.pause_at_end import run
    run(lambda: mpv_va_detect_play(input()))
