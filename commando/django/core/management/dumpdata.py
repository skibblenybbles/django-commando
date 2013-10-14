from commando import management


BaseDumpDataCommand = management.get_command_class(
    "dumpdata", exclude_packages=("commando",))

if BaseDumpDataCommand is not None:
    
    base = BaseDumpDataCommand()
    
    class DumpDataCommandOptions(management.CommandOptions):
        """
        Dump data command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[dumpdata options]",
                "These options will be passed to dumpdata.",
                option_list,
            ),) if option_list else ()
        actions = ("dumpdata",)
        
        def handle_dumpdata(self, *args, **options):
            return self.call_command("dumpdata", *args, **options)
    
    
    class DumpDataCommand(DumpDataCommandOptions, management.StandardCommand):
        """
        Dump data command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            DumpDataCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    DumpDataCommand = management.StandardCommand
