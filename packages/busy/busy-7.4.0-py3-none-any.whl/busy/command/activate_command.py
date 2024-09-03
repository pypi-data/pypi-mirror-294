from wizlib.parser import WizParser

from busy.command import QueueCommand
from busy.util import date_util


def is_today_or_earlier(plan):
    return plan.plan_date <= date_util.today()


class ActivateCommand(QueueCommand):

    timing: str = ""
    yes: bool = None
    collection_state: str = 'plan'
    name = 'activate'
    default_filter = [is_today_or_earlier]

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        # parser.add_argument('--timing', '-t', default='today')
        cls.add_yes_arg(parser)

    def handle_vals(self):
        super().handle_vals()
        if self.selection:
            if not self.provided('yes'):
                items = self.collection.items(self.selection)
                self.app.ui.send(self.selected_items_list)
                intro = f"Activate {self.summarize()}"
                self.confirm(intro)

    @QueueCommand.wrap
    def execute(self):
        todos = self.app.storage.get_collection(self.queue)
        activated = self.collection.delete(self.selection)
        for item in activated:
            item.state = 'todo'
        todos.extend(activated)
        self.status = f"Activated {self.summarize(activated)}"
