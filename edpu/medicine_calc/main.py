from .utils.data import Data
from typing import Any


def _main(data: Data) -> None:
    from .utils.daily_pcs import DailyPcs
    from codecs import StreamReaderWriter

    def operation_log(file: StreamReaderWriter, daily_pcs: DailyPcs) -> None:
        from .utils.stats import Stats

        file.write('Operation log\n\n')
        stats = Stats(data)

        for operation in data.operations:
            def handle() -> None:
                from .operations.consume import Consume
                from .operations.lose import Lose
                from .operations.restock import Restock
                from .utils.operation_type import OperationType

                def write_helper(data: str) -> None:
                    from .utils.mappers.operation_type_string import operation_type_to_string
                    file.write(f'{operation_type_to_string(operation.get_type())} {data}\n')

                def restock(operation: Restock) -> None:
                    from ..string_utils import merge_with_space
                    from .utils.pcs_pretty_print import pcs_pretty_print

                    stats.stock += operation.pcs

                    write_helper(merge_with_space([
                        pcs_pretty_print(operation.pcs, data),
                        'at',
                        operation.time
                    ]))

                def consume(operation: Consume) -> None:
                    from ..string_utils import merge_with_space
                    from .utils.pcs_pretty_print import pcs_pretty_print

                    stats.stock -= operation.pcs
                    stats.consumed += operation.pcs

                    daily_pcs.add(operation.pcs, operation.day, operation.day_part)

                    write_helper(merge_with_space([
                        pcs_pretty_print(operation.pcs, data),
                        'at',
                        operation.time,
                        'for',
                        operation.day,
                        operation.day_part
                    ]))

                def lose(operation: Lose) -> None:
                    from ..string_utils import merge_with_space
                    from .utils.pcs_pretty_print import pcs_pretty_print

                    stats.stock -= operation.pcs
                    stats.lost += operation.pcs

                    write_helper(merge_with_space([
                        pcs_pretty_print(operation.pcs, data),
                        'at',
                        operation.time
                    ]))

                {
                    OperationType.RESTOCK: restock,
                    OperationType.CONSUME: consume,
                    OperationType.LOSE: lose,
                }[operation.get_type()](operation)

            handle()
            file.write(stats.str() + '\n\n')

    def daily_report(file: StreamReaderWriter, daily_pcs: DailyPcs) -> None:
        file.write('\nDaily report\n')

        for str_ in daily_pcs.str():
            file.write(str_ + '\n')

    def impl() -> None:
        from codecs import open

        with open(data.report_file, 'w', 'utf-8') as file:
            daily_pcs = DailyPcs(data)
            operation_log(file, daily_pcs)
            daily_report(file, daily_pcs)

    impl()


def run(data_raw: dict[str, Any]) -> None:
    from .. import pause_at_end

    def impl() -> None:
        _main(Data(data_raw))

    pause_at_end.run(impl, pause_at_end.DEFAULT_MESSAGE)
