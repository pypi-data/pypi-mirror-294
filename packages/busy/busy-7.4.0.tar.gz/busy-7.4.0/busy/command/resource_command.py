from busy.command import CollectionCommand


class ResourceCommand(CollectionCommand):
    """Get the resource (URL) for items in a collection"""

    name = "resource"

    @CollectionCommand.wrap
    def execute(self):
        self.status = f"Listed {self.summarize()}"
        return self.output_items(lambda i: i.resource)
