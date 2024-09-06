from endstone import ColorFormat, Player
from endstone.command import Command, CommandSender

from endstone_essentials.commands.command_executor_base import CommandExecutorBase


class BackCommandExecutors(CommandExecutorBase):

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("This command can only be executed by a player")
            return False

        if sender.unique_id not in self.plugin.last_death_locations:
            sender.send_error_message(ColorFormat.DARK_RED + "It seems you haven't died yet.")
            return False

        location = self.plugin.last_death_locations[sender.unique_id]
        sender.teleport(location)
        sender.send_message(ColorFormat.GREEN + "You have been teleported to the last place of death")
        del self.plugin.last_death_locations[sender.unique_id]  # remove the last death location
        return True
