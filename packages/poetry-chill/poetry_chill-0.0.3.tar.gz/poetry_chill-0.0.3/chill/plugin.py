# import tomlkit
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from pip_chill import chill

command_name = "chill"


class ChillCommand(EnvCommand):
    name: str = command_name  # type: ignore

    def handle(self) -> int:
        self.line("Here we go!")
        distributions, _ = chill()
        # self.line(str(distributions))
        self.line("=====================")
        # path = self.poetry.file.path.absolute()
        # with open(path, "rb") as f:
        #     data = tomlkit.loads(f.read())

        for package in distributions:
            # data["tool"]["poetry"]["dependencies"][package.name] = package.version
            self.line(f"{package.name}")

        # with open(path, "w") as f:
        #     tomlkit.dump(data, f)
        return 0


class ChillPlugin(ApplicationPlugin):
    def activate(self, application) -> None:
        application.command_loader.register_factory(
            ChillCommand.name, lambda: ChillCommand()
        )
