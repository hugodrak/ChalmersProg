import gamemodel

""" Request input from the user """
def textInput(game):
    player = game.getCurrentPlayer()
    oldAngle, oldVel = player.getAim()
    print(player.getColor() + ' players turn!')
    print('The wind is howling at a good {0:.1f} speed'.format(game.getCurrentWind()))
    print('Previous angle was {0:.1f}, enter new angle'.format(oldAngle))
    newAngle = float(input())
    print('Previous velocity was {0:.1f}, enter new velocity'.format(oldVel))
    newVel = float(input())
    return newAngle, newVel

""" Fires a projectile for the current player and animates it until it stops
Returns the fired projectile """
def textFire(game, angle, vel):
    player = game.getCurrentPlayer()
    proj = player.fire(angle, vel)
    print('ball is moving ... ', end='')
    outputThrottle = 0
    while proj.isMoving():
        proj.update(1/50)
        if abs(player.projectileDistance(proj))>outputThrottle*10:
            print('{0:.1f} '.format(proj.getX()), end='')
            outputThrottle+=1
    print('')
    print('Impact at position {0:.1f}!'.format(proj.getX()))
    return proj

""" Shot cleanup, checks if the player hit its target, awards points and starts new rounds when appropriate and cycles to the next player """
def textFinishShot(game, proj):
    # The current player
    player = game.getCurrentPlayer()
    # The player opposing the current player
    other = game.getOtherPlayer()

    # Check if we won
    distance = other.projectileDistance(proj) 
    if distance == 0.0:
        print('Direct hit! ' + player.getColor() + ' player wins the round!')
        player.increaseScore()
        print('the current score is '+player.getColor()+':'+str(player.getScore())+', '+other.getColor()+':'+str(other.getScore()))
        # Start a new round
        game.newRound()
    else:
        print('missed by a distance of {0:.1f}'.format(distance))

    # Switch active player
    game.nextPlayer()
    
""" The main game loop """
def textPlay():
    game = gamemodel.Game(10,3)
    while True:
        angle, vel = textInput(game)
        proj = textFire(game, angle, vel)
        textFinishShot(game, proj)
        print("<press enter to continue>")
        input()
        print('') # Print an empty line

textPlay()