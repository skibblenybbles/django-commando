from commando import management


BaseCompileMessagesCommand = management.get_command_class(
    "compilemessages", exclude_packages=("commando",))

if BaseCompileMessagesCommand is not None:
    
    base = BaseCompileMessagesCommand()
    
    class CompileMessagesCommandOptions(management.CommandOptions):
        """
        Cleanup command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[compilemesssages options]",
                "These options will be passed to compilemessages.",
                option_list,
            ),) if option_list else ()
        actions = ("compilemessages",)
        
        def handle_compilemessages(self, *args, **options):
            return self.call_command("compilemessages", *args, **options)
    
    
    class CompileMessagesCommand(CompileMessagesCommandOptions, management.StandardCommand):
        """
        Shell command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CompileMessagesCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CompileMessagesCommand = management.StandardCommand
