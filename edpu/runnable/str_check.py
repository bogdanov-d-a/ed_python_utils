STR_CHECK = 'str_check'


if __name__ == '__main__':
    from edpu import pause_at_end

    def main() -> None:
        from edpu.input_to_output_file_conv import input_to_output_file_conv
        from edpu.str_check import str_check

        input_to_output_file_conv(
            f'{STR_CHECK}_input.tmp',
            f'{STR_CHECK}_output.tmp',
            str_check
        )

    pause_at_end.run(main, pause_at_end.DEFAULT_MESSAGE)
