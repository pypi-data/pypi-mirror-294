from random import choice

from busy.command import QueueCommand


class DropCommand(QueueCommand):
    """Move items to the end of the todo collection of a queue"""

    name = 'drop'
    default_filter = [1]

    def handle_vals(self):
        super().handle_vals()
        if self.selection:
            self.app.ui.send(self.selected_items_list)

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        lolist, hilist = self.collection.split(self.selection)
        self.collection.data = hilist + lolist
        self.status = f"Popped {self.summarize(lolist)}"


class PopCommand(QueueCommand):
    """Move items to the beginning of the collection"""

    name = 'pop'
    default_filter = ['-']

    def handle_vals(self):
        super().handle_vals()
        if len(self.selection) > 1:
            self.app.ui.send(self.selected_items_list)

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        hilist, lolist = self.collection.split(self.selection)
        self.collection.data = hilist + lolist
        self.status = f"Popped {self.summarize(hilist)}"


class PickCommand(QueueCommand):
    """Move a random item to the beginning of the collection"""

    name = 'pick'
    default_filter = ['-']

    @QueueCommand.wrap
    def execute(self):
        index = choice(self.selection)
        item = self.collection[index]
        hilist, lolist = self.collection.split([index])
        self.collection.data = hilist + lolist
        self.status = f"Picked {self.summarize([item])}"
