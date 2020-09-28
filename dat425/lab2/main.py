# Imports everything from both model and graphics
from gamegraphics import *


def graphicPlay():
    g = Game(cannonSize=20, ballSize=10)
    gg = GraphicGame(g)
    gg.run()


# Run the game with graphical interface
graphicPlay()
