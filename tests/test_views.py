from abc import ABC

from flask_testing import TestCase
from dashboard import create_app

class TestNotRenderTemplates(TestCase, ABC):
    render_templates = False

    def create_app(self):
        return create_app()

    # check if root url has the correct html called from template folder
    def test_assert_index_template_used(self):
        response = self.client.get("/")
        self.assert_template_used('index.html')

    # check if /user url has the correct html called from template folder
    def test_assert_user_template_used(self):
        response = self.client.get("/user")
        self.assert_template_used('user.html')

    # check if /analysis url has the correct html called from template folder
    def test_assert_analysis_template_used(self):
        response = self.client.get("/analysis")
        self.assert_template_used('analysis.html')

    # check if /bot url has the correct html called from template folder
    def test_assert_bot_template_used(self):
        response = self.client.get("/bot")
        self.assert_template_used('bot.html')

    # check if /custom_stream url has the correct html called from template folder
    def test_assert_custom_stream_template_used(self):
        response = self.client.get("/custom_stream")
        self.assert_template_used('stream.html')

    # check if /DIY_analysis url has the correct html called from template folder
    def test_assert_diy_analysis_template_used(self):
        response = self.client.get("/DIY_analysis")
        self.assert_template_used('DIY_analysis.html')

    # check if /DIY_visualization url has the correct html called from template folder
    def test_assert_DIY_visualization_template_used(self):
        response = self.client.get("/DIY_visualization")
        self.assert_template_used('DIY_visualization.html')
