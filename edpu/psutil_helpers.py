from typing import Iterator


def process_name_iter() -> Iterator[str]:
    from psutil import process_iter

    return map(
        lambda proc: proc.name(),
        process_iter()
    )


def process_names() -> set[str]:
    return set(process_name_iter())


def process_name_stat(name_filter: set[str]) -> dict[str, int]:
    result: dict[str, int] = { name: 0 for name in name_filter }

    for process_name in process_name_iter():
        if process_name in result:
            result[process_name] += 1

    return result
