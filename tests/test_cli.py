from abc import ABC

from flask_testing import TestCase
from dashboard import create_app
from dashboard.routes.cli import start_stream, profile


class TestCli(TestCase, ABC):
    ## create app function retuns the app with context
    def create_app(self):
        return create_app()

    def test_my_profile_cli(self):
        runner = create_app().test_cli_runner()

        # or by name
        result = runner.invoke(args=["cli","my_profile"])
        assert 'done' in result.output

    def test_stream_cli(self):
        runner = create_app().test_cli_runner()

        # or by name
        result = runner.invoke(args=["cli","start_stream"])
        assert 'done' in result.output