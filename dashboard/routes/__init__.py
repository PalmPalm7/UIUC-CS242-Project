from .main import main
from .analysis import analysis
from .bot import bot
from .stream import stream
from .DIY_analysis import DIY_analysis
from .DIY_visualization import  DIY_visualization
from .cli import cli

def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(analysis)
    app.register_blueprint(bot)
    app.register_blueprint(stream)

    app.register_blueprint(DIY_analysis)
    app.register_blueprint(DIY_visualization)
    app.register_blueprint(cli)
