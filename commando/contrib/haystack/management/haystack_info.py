from commando import management


BaseHaystackInfoCommand = management.get_command_class(
    "haystack_info", exclude_packages=("commando",))

if BaseHaystackInfoCommand is not None:
    
    base = BaseHaystackInfoCommand()
    
    class HaystackInfoCommandOptions(management.CommandOptions):
        """
        HaystackInfo command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[haystack_info options]",
                "These options will be passed to haystack_info.",
                option_list,
            ),) if option_list else ()
        actions = ("haystack_info",)
        
        def handle_haystack_info(self, *args, **options):
            return self.call_command("haystack_info", *args, **options)
    
    
    class HaystackInfoCommand(HaystackInfoCommandOptions, management.StandardCommand):
        """
        HaystackInfo command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            HaystackInfoCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    HaystackInfoCommand = management.StandardCommand
