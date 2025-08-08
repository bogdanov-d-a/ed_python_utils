MapConflict = dict[str, set[str]]
Map = dict[str, str]
Resolver = dict[str, tuple[str, str]]


def main() -> None:
    def get_map_conflict(fwd: bool, rev: bool) -> MapConflict:
        table = [
            ('`', 'ё'),
            ('~', 'Ё'),
            ('@', '"'),
            ('#', '№'),
            ('$', ';'),
            ('^', ':'),
            ('&', '?'),

            ('q', 'й'),
            ('w', 'ц'),
            ('e', 'у'),
            ('r', 'к'),
            ('t', 'е'),
            ('y', 'н'),
            ('u', 'г'),
            ('i', 'ш'),
            ('o', 'щ'),
            ('p', 'з'),
            ('[', 'х'),
            (']', 'ъ'),
            ('Q', 'Й'),
            ('W', 'Ц'),
            ('E', 'У'),
            ('R', 'К'),
            ('T', 'Е'),
            ('Y', 'Н'),
            ('U', 'Г'),
            ('I', 'Ш'),
            ('O', 'Щ'),
            ('P', 'З'),
            ('{', 'Х'),
            ('}', 'Ъ'),
            ('|', '/'),

            ('a', 'ф'),
            ('s', 'ы'),
            ('d', 'в'),
            ('f', 'а'),
            ('g', 'п'),
            ('h', 'р'),
            ('j', 'о'),
            ('k', 'л'),
            ('l', 'д'),
            (';', 'ж'),
            ('\'', 'э'),
            ('A', 'Ф'),
            ('S', 'Ы'),
            ('D', 'В'),
            ('F', 'А'),
            ('G', 'П'),
            ('H', 'Р'),
            ('J', 'О'),
            ('K', 'Л'),
            ('L', 'Д'),
            (':', 'Ж'),
            ('"', 'Э'),

            ('z', 'я'),
            ('x', 'ч'),
            ('c', 'с'),
            ('v', 'м'),
            ('b', 'и'),
            ('n', 'т'),
            ('m', 'ь'),
            (',', 'б'),
            ('.', 'ю'),
            ('/', '.'),
            ('Z', 'Я'),
            ('X', 'Ч'),
            ('C', 'С'),
            ('V', 'М'),
            ('B', 'И'),
            ('N', 'Т'),
            ('M', 'Ь'),
            ('<', 'Б'),
            ('>', 'Ю'),
            ('?', ','),
        ]

        result: MapConflict = {}

        def add(key: str, value: str) -> None:
            result.setdefault(key, set()).add(value)

        for en, ru in table:
            if fwd:
                add(en, ru)
            if rev:
                add(ru, en)

        return result

    def get_map(map_conflict: MapConflict, resolver: Resolver) -> Map:
        result: Map = {}

        for key, values in map_conflict.items():
            values_list = list(values)

            if len(values_list) == 1:
                result[key] = values_list[0]

            elif len(values_list) == 2:
                resolver_value = resolver[key]

                if set([resolver_value[0], resolver_value[1]]) != values:
                    raise Exception()

                result[key] = resolver_value[0]

            else:
                raise Exception()

        return result

    def proc_text(text: str, map: Map) -> str:
        result = ''

        for char in text:
            result += map.get(char, char)

        return result

    def get_dual_resolver() -> Resolver:
        return {
            '"': ('Э', '@'),
            ',': ('б', '?'),
            '.': ('ю', '/'),
            '/': ('.', '|'),
            ':': ('Ж', '^'),
            ';': ('ж', '$'),
            '?': (',', '&'),
        }

    def impl() -> None:
        from .window_processor import run_with_exception_wrappers

        def proc(text: str, fwd: bool, rev: bool, resolver: Resolver) -> str:
            return proc_text(
                text,
                get_map(
                    get_map_conflict(fwd, rev),
                    resolver
                )
            )

        run_with_exception_wrappers(
            [
                ('en -> ru', lambda text: proc(text, True, False, {})),
                ('ru -> en', lambda text: proc(text, False, True, {})),
                ('dual', lambda text: proc(text, True, True, get_dual_resolver())),
            ],
            'en_ru_converter'
        )

    impl()
