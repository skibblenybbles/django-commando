from commando import management


BaseFindStaticCommand = management.get_command_class(
    "findstatic", exclude_packages=("commando",))

if BaseFindStaticCommand is not None:
    
    base = BaseFindStaticCommand()
    
    class FindStaticCommandOptions(management.CommandOptions):
        """
        FindStatic command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[findstatic options]",
                "These options will be passed to findstatic.",
                option_list,
            ),) if option_list else ()
        actions = ("findstatic",)
        
        def handle_findstatic(self, *args, **options):
            return self.call_command("findstatic", *args, **options)
    
    
    class FindStaticCommand(FindStaticCommandOptions, management.StandardCommand):
        """
        FindStatic command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            FindStaticCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    FindStaticCommand = management.StandardCommand
