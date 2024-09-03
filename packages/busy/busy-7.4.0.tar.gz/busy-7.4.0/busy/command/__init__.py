from datetime import datetime

from wizlib.command import WizCommand
from wizlib.parser import WizParser
from wizlib.ui import Choice, Chooser
from wizlib.command import CommandCancellation

from busy.model.collection import Collection


class BusyCommand(WizCommand):

    default = 'null'

    # TODO: Move to wizlib
    @staticmethod
    def add_yes_arg(parser: WizParser):
        parser.add_argument('--yes', '-y', action='store_true', default=None)

    # TODO: Move to wizlib
    def confirm(self, verb, *other_actions):
        """Ensure that a command is confirmed by the user"""
        if self.provided('yes'):
            return self.yes
        else:
            def cancel():
                raise CommandCancellation('Cancelled')
            chooser = Chooser(f"{verb}?", 'OK', [
                Choice('OK', '\n', True),
                Choice('cancel', 'c', cancel)
            ])
            for action in other_actions:
                name = action.name if hasattr(action, 'name') else 'other'
                key = action.key if hasattr(action, 'key') else 'o'
                chooser.add_choice(name, key, action)
            choice = self.app.ui.get_option(chooser)
            if type(choice) is bool:
                self.yes = choice
            return choice


class QueueCommand(BusyCommand):
    """Base for commands that work on the default collection of one queue"""

    queue: str = 'tasks'
    collection_state: str = 'todo'
    filter: list = None
    default_filter = [1]
    named_filters: list = []
    selection_optional = False

    @property
    def collection(self):
        """Return the collection object being queried, usually todo"""
        if not hasattr(self, '_collection'):
            self._collection = self.app.storage.get_collection(
                self.queue, self.collection_state)
        return self._collection

    @property
    def complete_filter(self):
        """Simple filters plus named filters"""
        return self.filter + self.named_filters

    @property
    def selection(self):
        """Indices of objects within the query collection that match the
        filter"""
        if not hasattr(self, '_selection'):
            self._selection = self.collection.select(*self.complete_filter)
        return self._selection

    @property
    def selected_items(self):
        """Items in the selection"""
        return [self.collection[i] for i in self.selection]

    @property
    def selected_items_list(self):
        """Simple text list of selected items"""
        return '\n'.join([i.listable for i in self.selected_items])

    def time_value(self, minutes):
        """Estimated value of effort, usable for billable hours, rounded to one
        decimal place"""
        if not hasattr(self, '_multiplier'):
            self._multiplier = self.app.config.get('busy-multiplier') or 1.0
        return self._multiplier * minutes / 60.0

    def summarize(self, items: list = None):
        if items is None:
            items = self.selected_items
        if len(items) == 1:
            result = "1 item"
        elif len(items) > 1:
            result = str(len(items)) + " items"
        else:
            return "nothing"
        elapsed = sum(i.elapsed_time for i in items)
        if elapsed:
            # hours = int(elapsed/60)
            # minutes = elapsed % 60
            # if hours:
            #     result += f" ({hours}h{minutes}m"
            # else:
            #     result += f" ({minutes}m"
            result += f" ({self.time_value(elapsed):.1f})"
        return result

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--queue', '-q', default='tasks', nargs='?')
        parser.add_argument('filter', nargs="*")
        # parser.add_argument('--filter', '-f', action='store', nargs="*")

    def handle_vals(self):
        """Apply default filter"""
        super().handle_vals()
        if not self.provided('filter'):
            self.filter = self.default_filter

    @BusyCommand.wrap
    def execute(self, method, *args, **kwargs):
        """Handle timing and save operation"""
        if self.selection_optional or self.selection:
            if self.queue == 'tasks':
                todos = self.app.storage.get_collection('tasks', 'todo')
                if len(todos) > 0:
                    todos[0].update_time()
                    todos.changed = True
            result = method(self, *args, **kwargs)
            if self.queue == 'tasks':
                todos = self.app.storage.get_collection('tasks', 'todo')
                if len(todos) > 0:
                    todos[0].start_timer()
                    todos.changed = True
            self.app.storage.save()
            return result
        else:
            self.status = 'Empty set'


class CollectionCommand(QueueCommand):
    """Base for commands that work on a user-specified collection"""

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        states = Collection.family_attrs('state')
        parser.add_argument(
            '--state', '-s', action='store', default='todo',
            dest='collection_state', choices=states)

    def output_items(self, func, with_index=False):
        """Return some attribute of all the items in the collection"""
        if with_index:
            return '\n'.join(func(self.collection[i], i)
                             for i in self.selection)
        else:
            return '\n'.join(func(i) for i in self.selected_items)


class NullCommand(QueueCommand):
    name = 'null'

    @QueueCommand.wrap
    def execute(self):
        pass
