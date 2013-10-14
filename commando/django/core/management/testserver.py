from commando import management


BaseTestServerCommand = management.get_command_class(
    "testserver", exclude_packages=("commando",))

if BaseTestServerCommand is not None:
    
    base = BaseTestServerCommand()
    
    class TestServerCommandOptions(management.CommandOptions):
        """
        TestServer command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[testserver options]",
                "These options will be passed to testserver.",
                option_list,
            ),) if option_list else ()
        actions = ("testserver",)
        
        def handle_testserver(self, *args, **options):
            return self.call_command("testserver", *args, **options)
    
    
    class TestServerCommand(TestServerCommandOptions, management.StandardCommand):
        """
        TestServer command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            TestServerCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    TestServerCommand = management.StandardCommand
