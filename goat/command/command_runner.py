from subprocess import PIPE, run
from goat.command.command import Command
from goat.command.command_results import CommandResults


class CommandRunner:
    @staticmethod
    def run(command: Command) -> CommandResults:
        completed_process = run(command.to_list(), stdout=PIPE, stderr=PIPE, text=True)
        return CommandResults(
            completed_process.returncode,
            completed_process.stdout,
            completed_process.stderr,
        )
