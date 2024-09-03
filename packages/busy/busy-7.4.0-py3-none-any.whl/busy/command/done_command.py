from wizlib.parser import WizParser
from wizlib.command import CommandCancellation

from busy.command import QueueCommand
from busy.command.defer_command import Deferable
from busy.model.item import Item
from busy.util import date_util
from busy.util.date_util import relative_date


class DoneCommand(Deferable):
    """Combined the old defer and finish commands"""

    name = 'done'

    yes: bool = None
    when: str = ''

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('--defer', '-d', dest='when')
        cls.add_yes_arg(parser)

    def ask_defer(self):
        self.ask_when()
    ask_defer.name = 'defer'
    ask_defer.key = 'd'

    def ask_other(self):
        self.ask_when()
    ask_other.name = 'other'
    ask_other.key = 'o'

    def handle_vals(self):
        super().handle_vals()
        if self.selection:
            self.app.ui.send(self.selected_items_list)
            self.get_default_when()
            if self.provided('when'):
                if not self.check_when():
                    self.ask_when()
            if not self.provided('yes'):
                if not self.provided('yes'):
                    intro = f"Done {self.summarize()}"
                    if self.plan_date:
                        intro += f" and defer to {self.plan_date}"
                        self.confirm(intro, self.ask_other)
                    else:
                        self.confirm(intro, self.ask_defer)

    @QueueCommand.wrap
    def execute(self):
        date = date_util.today()
        dones = self.app.storage.get_collection(self.queue, 'done')
        plans = self.app.storage.get_collection(self.queue, 'plan')
        items = self.collection.delete(self.selection)
        nexts = [i.done(done_date=date_util.today(),
                        plan_date=self.plan_date) for i in items]
        nexts = [n for n in nexts if n]
        dones += items
        plans += nexts
        if self.plan_date:
            self.status = f"Done for now with {self.summarize(items)}"
            self.status += f" and deferred to {self.plan_date}"
        else:
            self.status = f"Finished {self.summarize(items)}"
