from commando import management


BaseCreateCacheTableCommand = management.get_command_class(
    "createcachetable", exclude_packages=("commando",))

if BaseCreateCacheTableCommand is not None:
    
    base = BaseCreateCacheTableCommand()
    
    class CreateCacheTableCommandOptions(management.CommandOptions):
        """
        Create cache table command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[createcachetable options]",
                "These options will be passed to createcachetable.",
                option_list,
            ),) if option_list else ()
        actions = ("createcachetable",)
        
        def handle_createcachetable(self, *args, **options):
            return self.call_command("createcachetable", *args, **options)
    
    
    class CreateCacheTableCommand(CreateCacheTableCommandOptions, management.StandardCommand):
        """
        Shell command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            CreateCacheTableCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    CreateCacheTableCommand = management.StandardCommand
