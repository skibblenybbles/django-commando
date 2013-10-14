from commando import management


BaseTestCommand = management.get_command_class(
    "test", exclude_packages=("commando",))

if BaseTestCommand is not None:
    
    base = BaseTestCommand()
    
    class TestCommandOptions(management.CommandOptions):
        """
        Test command options.
        
        """
        args = base.args
        help = base.help
        option_list = base.option_list[
            len(management.BaseCommandOptions.option_list):]
        option_groups = (
            ("[test options]",
                "These options will be passed to test.",
                option_list,
            ),) if option_list else ()
        actions = ("test",)
        
        def handle_test(self, *args, **options):
            return self.call_command("test", *args, **options)
    
    
    class TestCommand(TestCommandOptions, management.StandardCommand):
        """
        Test command.
        
        """
        option_list = management.StandardCommand.option_list
        option_groups = \
            TestCommandOptions.option_groups + \
            management.StandardCommand.option_groups
    
else:
    
    TestCommand = management.StandardCommand
