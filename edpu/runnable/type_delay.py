if __name__ == '__main__':
    from edpu.pynput_ex import ControllerEx, sleep
    c = ControllerEx()

    string = input()
    sleep()

    c.alt_tab()
    c.type_delay(string)
