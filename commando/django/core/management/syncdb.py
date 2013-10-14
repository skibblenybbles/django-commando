from commando import management


BaseSyncDBCommand = management.get_command_class(
    "syncdb", exclude_packages=("commando",))

if BaseSyncDBCommand is not None:
    
    base = BaseSyncDBCommand()
    
    class SyncDBCommandOptions(management.CommandOptions):
        """
        SyncDB command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[syncdb options]",
                "These options will be passed to syncdb.",
                option_list,
            ),) if option_list else ()
        actions = ("syncdb",)
        
        def handle_syncdb(self, *args, **options):
            return self.call_command("syncdb", *args, **options)
    
    
    class SyncDBCommand(SyncDBCommandOptions, management.StandardCommand):
        """
        SyncDB command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            SyncDBCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    SyncDBCommand = management.StandardCommand
