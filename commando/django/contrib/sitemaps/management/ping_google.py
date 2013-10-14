from commando import management


BasePingGoogleCommand = management.get_command_class(
    "ping_google", exclude_packages=("commando",))

if BasePingGoogleCommand is not None:
    
    base = BasePingGoogleCommand()
    
    class PingGoogleCommandOptions(management.CommandOptions):
        """
        PingGoogle command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[ping_google options]",
                "These options will be passed to ping_google.",
                option_list,
            ),) if option_list else ()
        actions = ("ping_google",)
        
        def handle_ping_google(self, *args, **options):
            return self.call_command("ping_google", *args, **options)
    
    
    class PingGoogleCommand(PingGoogleCommandOptions, management.StandardCommand):
        """
        PingGoogle command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            PingGoogleCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    PingGoogleCommand = management.StandardCommand
