from math import sin, cos, radians
import random


# TODO: Deal with all TODOs in this file and also remove the TODO and HINT comments.


class Game:
    """ This is the model of the game"""

    def __init__(self, cannonSize, ballSize):
        """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """

        # HINT: This constructor needs to create two players according to the rules specified in the assignment text
        self._cannon_size = cannonSize
        self._ball_size = ballSize

        self._players = [Player(
            self, -90, 0, True, 'blue'
        ), Player(
            self, 90, 0, False, 'red'
        )]

        # 0 for player1, 1 for player2
        self._active_player_index = 0

        self._wind_speed = 0

    def getPlayers(self):
        """ A list containing both players """

        return self._players

    def getCannonSize(self):
        """ The height/width of the cannon """
        return self._cannon_size

    def getBallSize(self):
        """ The radius of cannon balls """
        return self._ball_size

    def getCurrentPlayer(self):
        """ The current player, i.e. the player whose turn it is """
        return self._players[self._active_player_index]

    def getOtherPlayer(self):
        """ The opponent of the current player """

        return self._players[self._get_index_for_next_player()]

    def getCurrentPlayerNumber(self):
        """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
        return self._active_player_index

    def nextPlayer(self):
        """ Switch active player """
        self._active_player_index = self._get_index_for_next_player()

    def _get_index_for_next_player(self):
        """Returns the index for the next(other) player"""
        return (self._active_player_index + 1) % 2

    def setCurrentWind(self, wind):
        """ Set the current wind speed, only used for testing """

        self._wind_speed = wind

    def getCurrentWind(self):
        """ Returns the current wind speed"""
        return self._wind_speed

    def newRound(self):
        """ Start a new round with a random wind value (-10 to +10) """
        # HINT: random.random() gives a random value between 0 and 1
        # multiplying this by 20 gives a random value between 0 and 20
        # how do you shift a value between 0 and 20 to one between -10 and +10?

        new_wind = random.random() * 20 - 10
        self.setCurrentWind(new_wind)


class Player:
    """ Models a player """

    def __init__(self, game: Game, position_x: float, position_y: float, fire_to_right: bool, color: str):
        # HINT: It should probably take the Game that creates it as parameter and some additional properties that differ between players (like firing-direction, position and color)
        self._game = game
        self._color = color
        self._position_x = position_x
        self._position_y = position_y
        self._fire_to_right = fire_to_right

        self._score = 0

        self._aim_angle = 0
        self._aim_velocity = 0

    def fire(self, angle, velocity):
        """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
        # The projectile should start in the middle of the cannon of the firing player
        # HINT: Your job here is to call the constructor of Projectile with all the right values
        # Some are hard-coded, like the boundaries for x-position, others can be found in Game or Player

        if not self._fire_to_right:
            angle = 180 - angle

        proj = Projectile(angle, velocity, self._game.getCurrentWind(), self.getX(), self.getY() + self.get_size() / 2,
                          -1000, 1000)

        self._aim_angle = angle
        self._aim_velocity = velocity

        return proj

    def projectileDistance(self, proj):
        """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
        # HINT: both self (a Player) and proj (a Projectile) have getX()-methods.
        # HINT: This method should give a negative value if the projectile missed to the left and positive if it missed to the right.
        # The distance should be how far the projectile and cannon are from touching, not the distance between their centers.
        # You probably need to use getCannonSize and getBallSize from Game to compensate for the size of cannons/cannonballs

        # TODO: check what direction is positive / negative

        center_distance = proj.getX() - self.getX()

        collision_distance = self._game.getBallSize() + self.get_size() / 2

        if abs(center_distance) <= collision_distance:
            distance = 0
        else:
            if center_distance > 0:
                distance = center_distance - collision_distance
            else:
                distance = center_distance + collision_distance

        return distance

    def get_size(self) -> int:
        return self._game.getCannonSize()

    def getScore(self):
        """ The current score of this player """
        return self._score  # TODO: this is just a dummy value

    def increaseScore(self):
        """ Increase the score of this player by 1."""
        self._score += 1

    def getColor(self):
        """ Returns the color of this player (a string)"""
        return self._color  # TODO: this is just a dummy value

    def getX(self):
        """ The x-position of the centre of this players cannon """
        return self._position_x

    def getY(self):
        """ The y-position of the centre of this players cannon """
        return self._position_y

    def getAim(self):
        """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
        return self._aim_angle, self._aim_velocity


class Projectile:
    """ Models a projectile (a cannonball, but could be used more generally) """

    def __init__(self, angle: float, velocity, wind, xPos, yPos, xLower, xUpper):
        """
                Constructor parameters:
                angle and velocity: the initial angle and velocity of the projectile
                    angle 0 means straight east (positive x-direction) and 90 straight up
                wind: The wind speed value affecting this projectile
                xPos and yPos: The initial position of this projectile
                xLower and xUpper: The lowest and highest x-positions allowed
            """
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)
        self.wind = wind

    def update(self, time):
        """
            Advance time by a given number of seconds
            (typically, time is less than a second,
             for large values the projectile may move erratically)
        """
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8 * time
        xvel1 = self.xvel + self.wind * time

        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0

        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)

        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)

        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1

    def isMoving(self):
        """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    def getY(self):
        """ The current y-position (height) of the projectile". Should never be below 0. """
        return self.yPos
