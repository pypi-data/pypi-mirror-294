from busy.command import CollectionCommand

# Like base but with the tags


class SimpleCommand(CollectionCommand):

    name = "simple"

    @CollectionCommand.wrap
    def execute(self):
        self.status = f"Listed {self.summarize()}"
        return self.output_items(lambda i: i.simple)
