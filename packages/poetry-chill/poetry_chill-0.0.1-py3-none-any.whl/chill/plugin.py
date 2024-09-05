from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin, Application

command_name = "chill"


class ChillCommand(Command):
    name: str = command_name  # type: ignore

    def handle(self) -> int:
        self.line("Here we go!")
        return 0


class ChillPlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        application.command_loader.register_factory(
            ChillCommand.name, lambda: ChillCommand()
        )
