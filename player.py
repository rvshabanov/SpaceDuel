# Import modules
import os
from random import randint
import arcade
import numpy as np
import random

# My imports
import constants
import menus
import utils

"""
Player Sprite Class
Handles animation and movement
"""


class PlayerSprite(arcade.Sprite):
    """
    Player Sprite Class
    Init method - parameters:
                    ship        - ship name - folder to use to load sprites
                    max_speed   - maximum speed derived from Player
    """
    def __init__(self, ship, max_speed):
        super().__init__()

        # Set max speed
        self.max_speed = max_speed

        # Load ship Bitmaps
        self.textures = []
        texture = arcade.load_texture(utils.resource_path(os.path.join('data/' + ship, '0.png')))
        self.textures.append(texture)
        texture = arcade.load_texture(utils.resource_path(os.path.join('data/' + ship, '1.png')))
        self.textures.append(texture)
        texture = arcade.load_texture(utils.resource_path(os.path.join('data/' + ship, '2.png')))
        self.textures.append(texture)

        # By default, no flames
        self.set_texture(0)

        self.thrust_on = 0
        self.speed = np.array([0, 0])
        self.thrust = np.array([0, 0])

    """
    Player Sprite Class
    Update method - no parameters
    Handles movement and thrust animation
    """
    def update(self):
        # Handle movement
        self.change_x = self.speed[0]
        self.change_y = self.speed[1]

        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        # Calc thrust vector
        self.thrust = [np.sin(np.deg2rad(-self.angle)) / 10, np.cos(np.deg2rad(-self.angle)) / 10]
        # Add thrust vector to ships speed
        if self.thrust_on and self.speed[0] < self.max_speed and self.speed[1] < self.max_speed:
            self.speed = self.speed + self.thrust

        # Figure out if we should face left or right
        self.texture = self.textures[self.thrust_on]
        if self.thrust_on > 0:
            self.thrust_on += 1
            if self.thrust_on > 2:
                self.thrust_on = 1

        # Check against window boundaries
        # Leftmost
        if self.left < 0:
            self.left = 0
            self.speed[0] = - self.speed[0] * constants.BOUNCE_SPEED_RATIO

        # Rightmost
        elif self.right > constants.SCREEN_WIDTH - 1:
            self.right = constants.SCREEN_WIDTH - 1
            self.speed[0] = - self.speed[0] * constants.BOUNCE_SPEED_RATIO

        # Bottom
        if self.bottom < 0:
            self.bottom = 0
            self.speed[1] = - self.speed[1] * constants.BOUNCE_SPEED_RATIO

        # And top finally
        elif self.top > constants.SCREEN_HEIGHT - 1:
            self.top = constants.SCREEN_HEIGHT - 1
            self.speed[1] = - self.speed[1] * constants.BOUNCE_SPEED_RATIO


"""
Player Class
Handles gameplay for Player 1 and Player 2
"""


class ClassPlayer:
    """
    Player Class
    Init method -   parameters are:
                    name            - Player name
                    ship            - ship name and folder to load sprites from
                    x, y, r         - initial x and y in the window, r - initial angle of the ship
                    max_speed       - maximum speed ship can fly
                    rotation_speed  - rotation speed per keypress, degrees
                    acceleration    - acceleration per keypress
                    isAI            - is this ship an AI player? (NPC)
    """
    def __init__(self, name, ship, x, y, r, max_speed, rotation_speed, acceleration, isai):
        # Get init params and load to self
        self.name = name
        self.ship = ship
        self.max_speed = max_speed
        self.rotation_speed = rotation_speed
        self.acceleration = acceleration
        self.health = constants.MAX_HEALTH

        # Player sprite lists created
        self.sprite_list = arcade.SpriteList()

        # Players sprites
        self.sprite = PlayerSprite(ship, self.max_speed)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = r
        self.sprite_list.append(self.sprite)

        # is this player an AI
        self.isAI = isai

        # Init emitter used to draw explosions
        self.burst_texture = utils.resource_path(os.path.join('data/' + ship, 'burst.png'))
        self.emitters = []

        self.sound_laser = arcade.load_sound(utils.resource_path(os.path.join('data/' + ship, 'laser0.wav')))
        self.sound_mine = arcade.load_sound(utils.resource_path(os.path.join('data/' + ship, 'mine0.wav')))
        self.sound_boom = arcade.load_sound(utils.resource_path(os.path.join('data/' + ship, 'boom0.wav')))

        # Mines
        self.mines = arcade.SpriteList()

        # Bullets
        # Init bullet lists for player 1 and player 2
        self.bullets = arcade.SpriteList()
        self.cooldown = 0                                       # Cooldown counter
        self.bullet_cooldown = constants.BULLET_COOLDOWN        # Current cooldown setting (adjusted by powerups)

        # Player to Player collision on flag
        self.collision_on = True

    """
    Player Class
    Draw method -   no parameters
    Method is used to draw player's ship in the window. Called from GameView.on_draw()
    """
    def draw(self):
        self.sprite_list.draw()                         # Draw Player with animation (spaceship)
        self.mines.draw()                               # Draw mines
        self.bullets.draw()                             # Draw bullets

        # Burst Emitter
        for e in self.emitters:
            e.draw()

    """
    Player Class
    Rotate Clockwise -   no parameters
    """
    def rotate_cw(self):
        self.sprite.change_angle = -self.rotation_speed

    """
    Player Class
    Rotate Anti-ClockWise/Counter clockwise -   no parameters
    """
    def rotate_acw(self):
        self.sprite.change_angle = self.rotation_speed

    """
    Player Class
    Accelerate  -   no parameters
    """
    def accelerate(self):
        self.sprite.thrust_on = 1

    """
    Player Class
    Mine  -   no parameters
    Drop the mine
    """
    def mine(self):
        if len(self.mines) + 1 > constants.MAX_MINES:
            return

        mine = arcade.Sprite(utils.resource_path(os.path.join('data/' + self.ship, 'mine.png')), 0.3)
        mine.center_x = self.sprite.center_x
        mine.center_y = self.sprite.center_y

        mine.change_x = 0
        mine.change_y = 0
        mine.change_angle = 5

        self.mines.append(mine)
        arcade.play_sound(self.sound_mine)

    """
    Player Class
    Boom  -   no parameters
    Start emitter to display explosion
    """
    def boom(self):
        e = self.emitter_0()
        self.emitters.append(e)
        if len(self.emitters) > constants.MAX_EMITTERS:
            self.emitters.pop(0)

        arcade.play_sound(self.sound_boom)

    """
    Player Class
    Coast  -   no parameters
    Just coast in space without any acceleration
    """
    def coast(self):
        self.sprite.thrust_on = 0

    """
    Player Class
    Stop Rotation  -   no parameters
    Stops any rotation ongoing for the player
    """
    def stop_rotation(self):
        self.sprite.change_angle = 0

    """
    Player Class
    Update  -   parameters
                    other_player - other player instance to cross check for hits, etc.
                    powerups     - list of powerups to check if collected
                    window       - window instance to be able to call for arcade window methods
    All player logic goes here. Updates and hit checks.
    """
    def update(self, other_player, powerups, window):
        self.sprite_list.update()                   # Update Player sprite (spaceship)
        self.mines.update()                         # Update mines
        self.bullets.update()                       # Update bullets

        # Burst Emitter
        for e in self.emitters:
            e.update()

        # Cool down laser
        self.cooldown += 1

        # Calculate distance between players used below
        dx = self.sprite.center_x - other_player.sprite.center_x  # x difference
        dy = self.sprite.center_y - other_player.sprite.center_y  # y difference
        d = np.sqrt(np.square(dx) + np.square(dy))                 # distance - credit goes to Pythagoras

        # AI actions
        # Is it single player mode with AI enemy?
        if self.isAI:
            if dy != 0:
                a = np.rad2deg(np.arctan(dx/dy))                                  # Calc angle to aim in degrees
                if dy < 0:
                    self.sprite.angle = -a                                        # Set AI player's sprite angle
                else:
                    self.sprite.angle = -a - 180                                  # Set AI player's sprite angle

            # Accelerate if distance > 300 for close combat action
            if d > 300:
                self.accelerate()
            else:
                self.coast()

            # Shoot lasers randomly
            if not randint(0, constants.AI_SHOOT_PACE):
                self.shoot()

            # Drop mine randomly
            if not randint(0, constants.AI_SHOOT_PACE):
                self.mine()

        # END AI actions

        # PLAYER TO PLAYER COLLISION CHECK
        # Player 1 vs Player 2 collision
        # See above dx, dy, and d used in below calculations
        # The d line defines N-T coord system

        # Check if we are not overlapping P1 and P2 and turn on collision for players
        if d > self.sprite.width / 2 + other_player.sprite.width / 2 and \
           d > self.sprite.height / 2 + other_player.sprite.height / 2:
            self.collision_on = True

        # If players have collided and collision flag is on for both players:
        if arcade.check_for_collision(self.sprite, other_player.sprite) and \
           self.collision_on and other_player.collision_on:
            # Turn off collisions to avoid multiple collision events at the same time
            self.collision_on = False

            vx1 = self.sprite.speed[0]                                     # X component of velocity for Player 1
            vy1 = self.sprite.speed[1]                                     # Y component of velocity for Player 1

            vx2 = other_player.sprite.speed[0]                             # X component of velocity for Player 2
            vy2 = other_player.sprite.speed[1]                             # Y component of velocity for Player 2

            cos_fi = dx / d                                                # Cos Fi for coord system rotation
            sin_fi = dy / d                                                # Sin Fi for coord system rotation

            vn1 = vx1 * cos_fi + vy1 * sin_fi                              # Rotate coord system from XY to NT and
            vt1 = - vx1 * sin_fi + vy1 * cos_fi                            # calc Vn and Vt component of P1 veloc.

            vn2 = vx2 * cos_fi + vy2 * sin_fi                              # Rotate coord system from XY to NT and
            vt2 = - vx2 * sin_fi + vy2 * cos_fi                            # calc Vn and Vt component of P2 veloc.

            # During collision 2 objects exchange their Vn components of velocity
            # Thus, Vn1 goes to P1 and
            # Vn2 goes to P2
            dx1 = vn2 * cos_fi - vt1 * sin_fi                              # Rotate coord system back to window
            dy1 = vn2 * sin_fi + vt1 * cos_fi                              # system for P1 and calc DX and DY

            dx2 = vn1 * cos_fi - vt2 * sin_fi                              # Rotate coord system back to window
            dy2 = vn1 * sin_fi + vt2 * cos_fi                              # system for P2 and calc DX and DY

            self.sprite.speed[0] = dx1                                     # Load X and Y components of speed back
            self.sprite.speed[1] = dy1                                     # to player 1 sprite

            other_player.sprite.speed[0] = dx2                             # Load X and Y components of speed back
            other_player.sprite.speed[1] = dy2                             # to player 2 sprite

        # END COLLISION CHECKS
        # Extra variables used to give more clarity. Hope this helps...
        # See details in collision.xlsx Excel sheet

        # Check if player hits mine
        ship_hits = arcade.check_for_collision_with_list(self.sprite, other_player.mines)
        for hit in ship_hits:
            hit.remove_from_sprite_lists()                              # Get rid of the lucky mine
            self.boom()                                                 # Explosion
            self.health -= constants.MINE_DAMAGE                        # Do damage decreasing health

        # Check if any bullets have landed onto Players
        # Check Player 1 first
        ship_hits = arcade.check_for_collision_with_list(self.sprite, other_player.bullets)
        for hit in ship_hits:
            hit.remove_from_sprite_lists()                              # Get rid of the lucky bullet
            self.boom()                                                 # Explosion
            self.health -= constants.HIT_DAMAGE                         # Do damage decreasing health

        # DEATH IS INEVITABLE
        # If Player is out of health
        if self.health <= 0:
            if self.isAI == 0 and other_player.isAI == 0:                       # 2 Player game, other player wins
                game_over_view = menus.GameOverView(other_player.name + " wins!")
            elif self.isAI == 0 and other_player.isAI == 1:                     # Single player game, player loose
                game_over_view = menus.GameOverView("You loose! :(")
            else:                                                               # Single player game, player wins
                game_over_view = menus.GameOverView("You won! :)")

            window.show_view(game_over_view)

        # Check if player hit power-up
        ship_hits = arcade.check_for_collision_with_list(self.sprite, powerups)
        for hit in ship_hits:
            hit.remove_from_sprite_lists()                              # Get rid of the power up
            if self.bullet_cooldown > constants.POWERUP_EFFECT:
                self.bullet_cooldown -= constants.POWERUP_EFFECT        # Upgrade - decrease laser cool down time
            # Drop new powerup
            powerup = arcade.Sprite(utils.resource_path(os.path.join('data', 'powerup.png')), 0.3)
            powerup.center_x = randint(0 + 20, constants.SCREEN_WIDTH - 20)
            powerup.center_y = randint(0 + 20, constants.SCREEN_HEIGHT - 20)
            powerup.change_x = 0
            powerup.change_y = 0
            powerup.change_angle = -5
            powerups.append(powerup)

        # Get rid of bullets that flew out of the screen
        for bullet in self.bullets:
            if bullet.top < 0 or bullet.bottom > constants.SCREEN_HEIGHT or \
               bullet.right < 0 or bullet.left > constants.SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

    """
    Player Class
    Spawn Bullet  -   parameters:
                            angle - initial angle of the bullet
    """
    def shoot(self):
        if self.cooldown < self.bullet_cooldown:
            return

        self.cooldown = 0
        bullet = arcade.Sprite(utils.resource_path(os.path.join('data/' + self.ship, 'laser0.png')), 0.2)
        bullet.angle = self.sprite.angle
        bullet.center_x = self.sprite.center_x
        bullet.center_y = self.sprite.center_y

        bullet.change_x = np.cos(np.deg2rad(self.sprite.angle + 90)) * constants.BULLET_SPEED
        bullet.change_y = np.sin(np.deg2rad(self.sprite.angle + 90)) * constants.BULLET_SPEED

        self.bullets.append(bullet)
        arcade.play_sound(self.sound_laser)

    """
    Player Class
    emitter_0  -   no parameters
    Init emitter to display explosions
    """
    def emitter_0(self):
        """Burst, emit from center, particle with lifetime"""
        e = arcade.Emitter(
            center_xy=(self.sprite.center_x, self.sprite.center_y),
            emit_controller=arcade.EmitBurst(constants.BURST_PARTICLE_COUNT),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=self.burst_texture,
                change_xy=arcade.rand_in_circle((0.0, 0.0), constants.PARTICLE_SPEED_FAST),
                lifetime=random.uniform(constants.DEFAULT_PARTICLE_LIFETIME - 1.0, constants.DEFAULT_PARTICLE_LIFETIME),
                scale=constants.DEFAULT_SCALE,
                alpha=constants.DEFAULT_ALPHA
            )
        )
        return e
