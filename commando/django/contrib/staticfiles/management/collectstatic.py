from commando import management


BaseCollectStaticCommand = management.get_command_class(
    "collectstatic", exclude_packages=("commando",))

if BaseCollectStaticCommand is not None:
    
    base = BaseCollectStaticCommand()
    
    class CollectStaticCommandOptions(management.CommandOptions):
        """
        CollectStatic command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[collectstatic options]",
                "These options will be passed to collectstatic.",
                option_list,
            ),) if option_list else ()
        actions = ("collectstatic",)
        
        def handle_collectstatic(self, *args, **options):
            return self.call_command("collectstatic", *args, **options)
    
    
    class CollectStaticCommand(CollectStaticCommandOptions, management.StandardCommand):
        """
        CollectStatic command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CollectStaticCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CollectStaticCommand = management.StandardCommand
