# ------------------------------------------------------
# This module contains all graphics-classes for the game
# Most classes are wrappers around model classes, e.g.
#  * GraphicGame is a wrappoer around Game
#  * GraphicPlayer is a wrapper around Player
#  * GraphicProjectile is a wrapper around Projectile
# In addition there are two UI-classes that have no
# counterparts in the model:
#  * Button
#  * InputDialog
# ------------------------------------------------------


# This is the only place where graphics should be imported!
import random
from typing import Optional

from gamemodel import Game, Projectile, Player
from graphics import *


class GraphicGame:
    def __init__(self, game: Game):
        self._game = game

        # Create the game-window object
        self._win = GraphWin('Cannon game', 640, 480, autoflush=False)
        self._win.setCoords(-120, -10, 120, 155)

        # Draw the ground
        Line(Point(-100, 0), Point(100, 0)).draw(self._win)

        # loads the players from graphic player class
        self._players = {
            player: GraphicPlayer(player, self._win) for player in self._game.getPlayers()
        }

    def _get_graphicsplayer_from_player(self, player):
        return self._players[player]

    def next_player(self):
        self._game.nextPlayer()

    def getCurrentPlayer(self):
        return self._get_graphicsplayer_from_player(
            self._game.getCurrentPlayer()
        )

    def getPlayers(self):
        return list(self._players.values())

    def getCurrentPlayerNumber(self):
        return self._game.getCurrentPlayerNumber()

    def getOtherPlayer(self):
        return self._get_graphicsplayer_from_player(
            self._game.getOtherPlayer()
        )

    def getCurrentWind(self):
        return self._game.getCurrentWind()

    def setCurrentWind(self, val):
        return self._game.setCurrentWind(val)

    def nextPlayer(self):
        return self._game.nextPlayer()

    def newRound(self):
        self._game.newRound()

    def getWindow(self):
        return self._win

    def run(self):
        """Run the main game-loop"""
        while True:

            player = self.getCurrentPlayer()
            aim, velocity = player.getAim()

            # Get shoot-input from user
            dialog = InputDialog(aim, velocity, self.getCurrentWind())

            action, angle, velocity = dialog.interact()
            dialog.close()

            if action == "Quit":
                break

            gproj = player.fire(angle, velocity)
            while gproj.isMoving():
                gproj.update(1 / 50)
                update(200)

            if self.getOtherPlayer().projectileDistance(gproj) == 0:
                # We have a hit
                player.increaseScore()
                self.newRound()

            self.nextPlayer()


class GraphicPlayer:
    def __init__(self, player: Player, window: GraphWin):
        self.player = player
        self.window = window

        x = self.player.getX()
        size = player.get_size()

        # Bounding size of the cannon
        cannon_rect = Rectangle(
            Point(x - size / 2, 0), Point(x + size / 2, size)
        )

        cannon_rect.setFill(self.player.getColor())
        cannon_rect.draw(self.window)

        self._score_label = Text(Point(x, -5), '')
        self._score_label.draw(self.window)
        self._update_score_label()

        self._cannon_rect = cannon_rect

        self._projectile: Optional[GraphicProjectile] = None

    def fire(self, angle, vel):
        # Fire the cannon of the underlying player object
        proj = self.player.fire(angle, vel)

        if self._projectile is not None:
            self._projectile.remove()

        self._projectile = GraphicProjectile(proj, self)

        return self._projectile

    def getAim(self):
        return self.player.getAim()

    def getColor(self):
        return self.player.getColor()

    def getX(self):
        return self.player.getX()

    def getScore(self):
        return self.player.getScore()

    def projectileDistance(self, proj):
        return self.player.projectileDistance(proj)

    def increaseScore(self):
        self.player.increaseScore()
        self._update_score_label()

    def _update_score_label(self):
        """Updates the score-label on screen"""
        self._score_label.setText(f'Score: {self.player.getScore()}')

    def get_ball_size(self) -> int:
        return self.player.get_ball_size()


class GraphicProjectile:
    """ A graphic wrapper around the Projectile class (adapted from ShotTracker in book)"""

    def __init__(self, projectile: Projectile, player: GraphicPlayer):
        self.proj = projectile
        self.player = player
        self._graphics_circle = None
        self.draw()

    def update(self, dt):
        # update the projectile
        self.proj.update(dt)
        self.remove()
        self.draw()

    def getX(self):
        return self.proj.getX()

    def getY(self):
        return self.proj.getY()

    def isMoving(self):
        return self.proj.isMoving()

    def draw(self):
        self._graphics_circle = Circle(Point(self.getX(), self.getY()), self.player.get_ball_size())
        self._graphics_circle.setFill(self.player.getColor())
        self._graphics_circle.draw(self.player.window)

    def remove(self):
        self._graphics_circle.undraw()


class InputDialog:
    """ A somewhat specific input dialog class (adapted from the book) """

    def __init__(self, angle, vel, wind):
        """ Takes the initial angle and velocity values, and the current wind value """
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0, 5.5, 4, .5)
        Text(Point(1, 1), "Angle").draw(win)
        self.angle = Entry(Point(3, 1), 5).draw(win)
        self.angle.setText(str(angle))

        Text(Point(1, 2), "Velocity").draw(win)
        self.vel = Entry(Point(3, 2), 5).draw(win)
        self.vel.setText(str(vel))

        Text(Point(1, 3), "Wind").draw(win)
        self.height = Text(Point(3, 3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))

        self.fire = Button(win, Point(1, 4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3, 4), 1.25, .5, "Quit")
        self.quit.activate()
        self.random = Button(win, Point(1, 5), 1.75, .5, "Random fire!")
        self.random.activate()

    def interact(self):
        """ Runs a loop until the user presses either the quit or fire button,
            returns a tuple of what action the user selected, the current angle and velocity
         """
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit", None, None
            if self.fire.clicked(pt):
                return "Fire!", float(self.angle.getText()), float(self.vel.getText())
            if self.random.clicked(pt):
                return "Fire! random", random.random() * 70 + 10, random.random() * 50 + 10

    def close(self):
        """ Returns the current values of (angle, velocity) as entered by the user"""
        self.win.close()


class Button:
    """ A general button class (from the book) """

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """

        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "RETURNS true if button active and p is inside"
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "RETURNS the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0
