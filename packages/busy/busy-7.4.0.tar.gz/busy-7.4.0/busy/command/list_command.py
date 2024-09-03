from wizlib.parser import WizParser

from busy.command import CollectionCommand
from busy.util.date_util import absolute_date


class ListCommand(CollectionCommand):
    """Show the descriptions with selection numbers, default to all"""

    name = 'list'
    default_filter = ['1-']
    FORMATS = {
        'description': "{!s}",
        'plan_date': "{:%Y-%m-%d}",
        'done_date': "{:%Y-%m-%d}"
    }

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        # parser.add_argument('--extended', '-x', action='store_true')
        parser.add_argument('--done_min', '--done-min')
        parser.add_argument('--done_max', '--done-max')

    def handle_vals(self):
        super().handle_vals()
        self.named_filters = []
        if self.provided('done_min'):
            def minfunc(i): return i.done_date >= absolute_date(self.done_min)
            self.named_filters.append(minfunc)
        if self.provided('done_max'):
            def maxfunc(i): return i.done_date <= absolute_date(self.done_max)
            self.named_filters.append(maxfunc)

    @CollectionCommand.wrap
    def execute(self):
        def format(item, index):
            result = f"{(index+1):>6}"
            for colname in self.collection.schema:
                format = self.FORMATS[colname]
                if (colname == 'description'):
                    value = item.listable
                else:
                    value = getattr(item, colname)
                result += f"  {format.format(value)}"
            return result
        self.status = f"Listed {self.summarize()}"
        return self.output_items(format, with_index=True)
