# Import modules
from random import randint
import os
import pyglet.media as pm
import json

# My imports
import constants
import arcade
import player
import menus
import utils

"""
Main Game View
All game actions, key press handler and updates are here
"""


class GameView(arcade.View):
    """
    Game View Class
    Init method - parameters:
                    game_mode   -   Game mode is 0 for 2 player game, 1 for single player, 2 - 2 player LAN
    """
    def __init__(self, game_mode, *n):
        super().__init__()

        # LAN game related
        if n:
            self.n = n[0]

        self.p2pos = {
            "other_id": 0,
            "center_x": 0,
            "center_y": 0,
            "change_x": 0,
            "change_y": 0,
            "angle": 0,
            "thrust_on": 0,
            "health": 0,
            "event": "None",

        }

        self.lan_errors = 0
        self.response = ""

        # Set game mode
        self.game_mode = game_mode                      # 0 - 2 player game, 1 - 2nd player is AI, 2 - LAN game server
        # Set background to black, init backgrounds list,
        # and set background to None
        arcade.set_background_color(arcade.color.BLACK)
        self.backgrounds = [
            utils.resource_path(os.path.join('data/bg', 'bg0.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg1.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg2.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg3.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg4.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg5.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg6.jpg')),
            utils.resource_path(os.path.join('data/bg', 'bg7.jpg')),
        ]
        self.background = None

        # Background music
        self.music = pm.load(utils.resource_path(os.path.join('data', 'music1.wav')))
        self.player = pm.Player()
        self.player.queue(self.music)
        self.player.play()

        # Powerups
        # Init power ups list
        self.powerups = arcade.SpriteList()

        # Create 2 player objects, position them to different edges of the window, set initial speed
        # Player 1
        # Parameters: ship, x, y, r, max_speed, rotation_speed, acceleration, isAI
        if self.game_mode == 3:
            self.player1 = player.ClassPlayer("Player 1", "cobra",
                                              0 + constants.SPRITE_SIZE,
                                              constants.SCREEN_HEIGHT / 2 + constants.SPRITE_SIZE * 2, -90,
                                              constants.MAX_SPEED, constants.MAX_ROTATION_SPEED, constants.ACCELERATION,
                                              self.game_mode)
            self.player1.sprite.speed[0] = 0.01  # Initial motion speed
            self.player1.sprite.thrust_on = 1  # Initial thrust is on
        else:
            self.player1 = player.ClassPlayer("Player 1", "cobra",
                                              constants.SCREEN_WIDTH - constants.SPRITE_SIZE,
                                              constants.SCREEN_HEIGHT / 2 - constants.SPRITE_SIZE * 2, 90,
                                              constants.MAX_SPEED, constants.MAX_ROTATION_SPEED, constants.ACCELERATION,
                                              0)
            self.player1.sprite.speed[0] = -0.01              # Initial motion speed
            self.player1.sprite.thrust_on = 1                 # Initial thrust is on

        # Player 2
        # Game mode affects player2 creation - AI or not
        # Parameters: ship, x, y, r, max_speed, rotation_speed, acceleration, isAI
        if self.game_mode == 1:
            name2nd = "alien"
        else:
            name2nd = "viper"
        self.player2 = player.ClassPlayer("Player 2", name2nd,
                                          0 + constants.SPRITE_SIZE,
                                          constants.SCREEN_HEIGHT / 2 + constants.SPRITE_SIZE * 2, -90,
                                          constants.MAX_SPEED, constants.MAX_ROTATION_SPEED, constants.ACCELERATION,
                                          self.game_mode)
        self.player2.sprite.speed[0] = 0.01               # Initial motion speed
        self.player2.sprite.thrust_on = 1                 # Initial thrust is on

        # Set random background from backgrounds list
        self.background = arcade.load_texture(self.backgrounds[randint(0, len(self.backgrounds) - 1)])

        # Setup power-ups list
        for i in range(0, constants.MAX_POWERUPS):
            powerup = arcade.Sprite(utils.resource_path(os.path.join('data', 'powerup.png')), 0.3)
            powerup.center_x = randint(0 + 20, constants.SCREEN_WIDTH - 20)
            powerup.center_y = randint(0 + 20, constants.SCREEN_HEIGHT - 20)
            # Initial power-up motion is 0, rotation is -5 degrees per cycle
            powerup.change_x = 0
            powerup.change_y = 0
            powerup.change_angle = -5
            # Append power-up to power-ups list
            self.powerups.append(powerup)

    """
    Game View Class
    On_Draw method - Render all objects in the window
    """
    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the background
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.background)

        # Call draw() on both player objects...
        self.player1.draw()
        self.player2.draw()
        # ... and power-ups finally.
        self.powerups.draw()

        # Draw health bars
        # Player 2
        draw_health_bar(10, self.player2.health + 10,
                        constants.SCREEN_HEIGHT - 10, constants.SCREEN_HEIGHT - 30, self.player2.health)
        # Player 1
        draw_health_bar(constants.SCREEN_WIDTH - self.player1.health - 10, constants.SCREEN_WIDTH - 10,
                        constants.SCREEN_HEIGHT - 10, constants.SCREEN_HEIGHT - 30, self.player1.health)

    """
    Game View Class
    On_Update method - Call update methods of player instances, etc.
    """
    def on_update(self, delta_time):
        # Check if LAN game
        if self.game_mode >= 2 and self.n:
            self.lan_exchange()
            # check if client is still there
            if self.game_mode == 2:
                (e, self.response) = self.n.send("POLL")
                if int(self.response) < 3:
                    disconnected_view = menus.DisconnectedView()  # Show LAN Game disconnected screen
                    self.window.show_view(disconnected_view)

        # Call update on player objects...
        self.player1.update(self.player2, self.powerups, self.window)       # Player 1 logic
        self.player2.update(self.player1, self.powerups, self.window)       # Player 2 logic

        # Update power-ups
        self.powerups.update()

        # Restart music if it is over
        if not self.player.playing:
            self.player.queue(self.music)
            self.player.play()

        # Kill music if game over
        if self.player1.health <= 0 or self.player2.health <= 0:
            self.player.delete()

    """
    Game View Class
    On_Key_Press - All key handling is here
    """
    def on_key_press(self, key, key_modifiers):
        """
        General controls
        """
        if key == arcade.key.ESCAPE or key == arcade.key.P:
            pause_view = menus.PauseView(self)                      # Pause screen
            self.window.show_view(pause_view)

        """
        Player 1 controls
        """
        if key == arcade.key.UP:
            self.player1.accelerate()
        elif key == arcade.key.DOWN:
            self.player1.mine()
            if self.game_mode >= 2:             # Deal with LAN game
                self.p2pos["event"] = "mine"
        elif key == arcade.key.LEFT:
            self.player1.rotate_acw()
        elif key == arcade.key.RIGHT:
            self.player1.rotate_cw()
        elif key == arcade.key.RIGHT:
            self.player1.rotate_cw()
        elif key == arcade.key.INSERT:
            self.player1.shoot()
            if self.game_mode >= 2:             # Deal with LAN game
                self.p2pos["event"] = "shoot"

        """
        Player 2 controls
        The difference is check for game mode. In case of single player game do nothing here
        """
        if self.game_mode == 0:
            if key == arcade.key.W:
                self.player2.accelerate()
            elif key == arcade.key.S:
                self.player2.mine()
            elif key == arcade.key.A:
                self.player2.rotate_acw()
            elif key == arcade.key.D:
                self.player2.rotate_cw()
            elif key == arcade.key.TAB:
                self.player2.shoot()

    """
    Game View Class
    On_Key_Release - Some key release events are here
    """
    def on_key_release(self, key, key_modifiers):
        """
        Player 1 controls
        """
        if key == arcade.key.UP:
            self.player1.coast()
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player1.stop_rotation()
        """
        Player 2 controls
        The difference is check for game mode. In case of single player game do nothing here
        """
        if not self.game_mode:
            if key == arcade.key.W:
                self.player2.coast()
            if key == arcade.key.A or key == arcade.key.D:
                self.player2.stop_rotation()

    """
    Game View Class
    LAN Exchange - send own data to server and get back other player's data
    """
    def lan_exchange(self):
        # Send self data
        self.p2pos["center_x"] = self.player1.sprite.center_x
        self.p2pos["center_y"] = self.player1.sprite.center_y
        self.p2pos["change_x"] = self.player1.sprite.speed[0]
        self.p2pos["change_y"] = self.player1.sprite.speed[1]
        self.p2pos["angle"] = self.player1.sprite.angle
        self.p2pos["thrust_on"] = self.player1.sprite.thrust_on
        self.p2pos["health"] = self.player1.health

        # Encode self data and send to server
        s = json.dumps(self.p2pos, default=utils.myconverter)
        (e, s) = self.n.send(s)

        # check if error occurred
        if e != 0:
            self.lan_errors += 1
            if self.lan_errors > constants.MAX_LAN_ERRORS:
                disconnected_view = menus.DisconnectedView()  # Show LAN Game disconnected screen
                self.window.show_view(disconnected_view)
        else:
            self.lan_errors = 0

        # Try to json decode the response and load data of other player
        try:
            self.p2pos = json.loads(s)

            # Load received date for other player
            self.player2.sprite.center_x = self.p2pos["center_x"]
            self.player2.sprite.center_y = self.p2pos["center_y"]
            self.player2.sprite.speed[0] = self.p2pos["change_x"]
            self.player2.sprite.speed[1] = self.p2pos["change_y"]
            self.player2.sprite.angle = self.p2pos["angle"]
            self.player2.sprite.thrust_on = self.p2pos["thrust_on"]
            self.player2.health = self.p2pos["health"]
            if self.p2pos["event"] == "shoot":
                self.player2.shoot()
            elif self.p2pos["event"] == "mine":
                self.player2.mine()

        except json.decoder.JSONDecodeError as e:
            # Json loads failed - probably transmission issue or format issue
            print("JSON Decode error: ", e)

        # Set event to none
        self.p2pos["event"] = "None"


"""
Static draw_health_bars
Draw Health Bars for players. Parameters: coords of left, right, top, bottom and health value 
"""


def draw_health_bar(left, right, top, bottom, health):
    if int(health / constants.MAX_HEALTH * 100) < 30:
        color = arcade.color.RED                            # Health < 30% - RED
    elif int(health / constants.MAX_HEALTH * 100) < 50:
        color = arcade.color.ORANGE                         # Health < 50% - ORANGE
    else:
        color = arcade.color.GREEN                          # else - GREEN
    arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, color)
