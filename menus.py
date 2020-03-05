# Import modules
import arcade
import os
import pyglet.media as pm

# My imports
import constants
import gameview
import utils


"""
Menu View Class
Main menu view
"""


class MenuView(arcade.View):
    """
    Menu View Class
    Init method -   no parameters
    """
    def __init__(self):
        super().__init__()

        self.menu = [
            "1 Player",
            "2 Players",
            "Controls",
            "Exit",
        ]

        self.menu_item_selected = 0

        # Background music
        self.music = pm.load(utils.resource_path(os.path.join('data', 'music0.wav')))
        self.player = pm.Player()
        self.player.queue(self.music)
        self.player.play()

    """
    Menu View Class
    On Show method -   no parameters
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    """
    Menu View Class
    On Draw method -   no parameters
    Draw background and menu items
    """
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                                            arcade.load_texture(utils.resource_path(os.path.join('data/bg',
                                                                                                 'bg_menu.jpg'))))

        v_offset = (len(self.menu) - 1) * 50
        for i in range(0, len(self.menu)):
            color = arcade.color.WHITE
            if i == self.menu_item_selected:
                color = arcade.color.YELLOW
            arcade.draw_text(self.menu[i], constants.SCREEN_WIDTH / 2,
                             (constants.SCREEN_HEIGHT + v_offset) / 2 - i * 60,
                             color, font_size=50, anchor_x="center")

    """
    Menu View Class
    On Key Press -   parameters:
                        key             - key code
                        _modifiers      - modifiers, i.e. shift, ctrl, etc.
                        see arcade docs for details
    Handles key presses in the main menu
    """
    def on_key_press(self, key, _modifiers):

        if key == arcade.key.DOWN and self.menu_item_selected < len(self.menu) - 1:
            self.menu_item_selected += 1

        if key == arcade.key.UP and self.menu_item_selected > 0:
            self.menu_item_selected -= 1

        if key == arcade.key.ENTER:
            if self.menu[self.menu_item_selected] == "1 Player":
                self.player.delete()                                # Stop background music
                difficulty_view = DifficultyView()                    # Show Difficulty selection screen
                self.window.show_view(difficulty_view)

            if self.menu[self.menu_item_selected] == "2 Players":
                self.player.delete()                                # Stop background music
                game_view = gameview.GameView(0)                    # Start two player game on same keyboard
                self.window.show_view(game_view)

            if self.menu[self.menu_item_selected] == "Controls":
                controls_view = ControlsView()                      # Show Controls screen
                self.window.show_view(controls_view)

            if self.menu[self.menu_item_selected] == "Exit":
                arcade.close_window()                               # Sayonara!

    """
    Menu View Class
    On Update  -   no parameters
    Handles updates while in the main menu
    """
    def on_update(self, delta_time):
        # Restart music if it is over
        if not self.player.playing:
            self.player.queue(self.music)
            self.player.play()


"""
Difficulty View Class
Difficulty menu view
"""


class DifficultyView(arcade.View):
    """
    Difficulty View Class
    Init method -   no parameters
    """
    def __init__(self):
        super().__init__()

        self.menu = [
            "Easy",
            "Medium",
            "Hard",
            "Nightmare",
        ]

        self.menu_item_selected = 1

    """
    Difficulty View Class
    On Show method -   no parameters
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    """
    Difficulty View Class
    On Draw method -   no parameters
    Draw background and menu items
    """
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
                                            arcade.load_texture(utils.resource_path(os.path.join('data/bg',
                                                                                                 'bg_menu.jpg'))))

        v_offset = (len(self.menu) - 1) * 50
        for i in range(0, len(self.menu)):
            color = arcade.color.WHITE
            if i == self.menu_item_selected:
                color = arcade.color.YELLOW
            arcade.draw_text(self.menu[i], constants.SCREEN_WIDTH / 2,
                             (constants.SCREEN_HEIGHT + v_offset) / 2 - i * 60,
                             color, font_size=50, anchor_x="center")

    """
    Difficulty View Class
    On Key Press -   parameters:
                        key             - key code
                        _modifiers      - modifiers, i.e. shift, ctrl, etc.
                        see arcade docs for details
    Handles key presses in the main menu
    """
    def on_key_press(self, key, _modifiers):

        if key == arcade.key.DOWN and self.menu_item_selected < len(self.menu) - 1:
            self.menu_item_selected += 1

        if key == arcade.key.UP and self.menu_item_selected > 0:
            self.menu_item_selected -= 1

        if key == arcade.key.ENTER:
            if self.menu[self.menu_item_selected] == "Easy":
                constants.AI_SHOOT_PACE = constants.AI_EASY_SHOOT_PACE
                constants.AI_PREDICTIVE = 0
                game_view = gameview.GameView(1)                    # Start single player game vs AI
                self.window.show_view(game_view)
            if self.menu[self.menu_item_selected] == "Medium":
                constants.AI_SHOOT_PACE = constants.AI_MEDIUM_SHOOT_PACE
                constants.AI_PREDICTIVE = 0
                game_view = gameview.GameView(1)                    # Start single player game vs AI
                self.window.show_view(game_view)
            if self.menu[self.menu_item_selected] == "Hard":
                constants.AI_SHOOT_PACE = constants.AI_HARD_SHOOT_PACE
                constants.AI_PREDICTIVE = 0
                game_view = gameview.GameView(1)                    # Start single player game vs AI
                self.window.show_view(game_view)
            if self.menu[self.menu_item_selected] == "Nightmare":
                constants.AI_SHOOT_PACE = constants.AI_NIGHTMARE_SHOOT_PACE
                constants.AI_PREDICTIVE = 1
                game_view = gameview.GameView(1)                    # Start single player game vs AI
                self.window.show_view(game_view)

    """
    Difficulty View Class
    On Update  -   no parameters
    Handles updates while in the main menu
    """
    def on_update(self, delta_time):
        pass


"""
Controls View Class
Controls menu view
"""


class ControlsView(arcade.View):
    """
    Controls View Class
    On Show Method - no parameters
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    """
    Controls View Class
    On Draw Method - no parameters
    Draws background and controls for Player 1 and Player 2
    """
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Player 1", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2 + 150,
                         arcade.color.BLACK, font_size=50, anchor_x="right")
        arcade.draw_text("Rotate Left - ←", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2 + 100,
                         arcade.color.BLACK, font_size=36, anchor_x="right")
        arcade.draw_text("Rotate Right - →", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=36, anchor_x="right")
        arcade.draw_text("Accelerate - ↑", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=36, anchor_x="right")
        arcade.draw_text("Drop Mine - ↓", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=36, anchor_x="right")
        arcade.draw_text("Shoot- INS", constants.SCREEN_WIDTH / 2 - 50, constants.SCREEN_HEIGHT / 2 - 100,
                         arcade.color.BLACK, font_size=36, anchor_x="right")

        arcade.draw_text("Player 2", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2 + 150,
                         arcade.color.BLACK, font_size=50, anchor_x="left")
        arcade.draw_text("A - Rotate Left", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2 + 100,
                         arcade.color.BLACK, font_size=36, anchor_x="left")
        arcade.draw_text("D - Rotate Right", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=36, anchor_x="left")
        arcade.draw_text("W - Accelerate", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=36, anchor_x="left")
        arcade.draw_text("S - Drop Mine", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=36, anchor_x="left")
        arcade.draw_text("TAB - Shoot", constants.SCREEN_WIDTH / 2 + 50, constants.SCREEN_HEIGHT / 2 - 100,
                         arcade.color.BLACK, font_size=36, anchor_x="left")

        arcade.draw_text("Press Enter for main menu", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    """
    Controls View Class
    On Key Press -   parameters:
                        key             - key code
                        _modifiers      - modifiers, i.e. shift, ctrl, etc.
                        see arcade docs for details
    Handles key presses in the controls menu
    """
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            menu_view = MenuView()
            self.window.show_view(menu_view)


"""
Game Over View Class
Game over screen
"""


class GameOverView(arcade.View):
    """
    Game Over View Class
    Init  -   parameters:
                        player_won             - text, who wins?
    """
    def __init__(self, player_won):
        super().__init__()
        self.player_won = player_won

    """
    Game Over View Class
    On Show method  -   no parameters
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    """
    Game Over View Class
    On Draw method  -   no parameters
    Draws game over text and who have won.
    """
    def on_draw(self):
        arcade.start_render()
        # Game over message
        arcade.draw_text("Game Over", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 + 50, arcade.color.BLACK, 50,
                         width=constants.SCREEN_WIDTH, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text(self.player_won, constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 50,
                         arcade.color.BLACK, 36, width=constants.SCREEN_WIDTH,
                         align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ESC to continue...", constants.SCREEN_WIDTH/2, 50, arcade.color.BLACK, 24,
                         width=constants.SCREEN_WIDTH, align="center", anchor_x="center", anchor_y="center")

    """
    Game Over View Class
    On Key Press method -   parameters:
                        key             - key code
                        _modifiers      - modifiers, i.e. shift, ctrl, etc.
                        see arcade docs for details
    Handles key presses in the game over screen
    """
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


"""
Pause View Class
Pause game view
"""


class PauseView(arcade.View):
    """
    Pause View Class
    Init -   parameters:
                        game_view             - GameView class instance
    Uses game_view to be able to return to game window.
    """
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    """
    Pause View Class
    On Show  -   no parameters
    """
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    """
    Pause View Class
    On Draw  -   no parameters
    Renders pause screen text and key hints
    """
    def on_draw(self):
        arcade.start_render()

        player1_sprite = self.game_view.player1.sprite
        player1_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player1_sprite.left,
                                          right=player1_sprite.right,
                                          top=player1_sprite.top,
                                          bottom=player1_sprite.bottom,
                                          color=arcade.color.ORANGE + (200,))

        player2_sprite = self.game_view.player2.sprite
        player2_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player2_sprite.left,
                                          right=player2_sprite.right,
                                          top=player2_sprite.top,
                                          bottom=player2_sprite.bottom,
                                          color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to continue",
                         constants.SCREEN_WIDTH / 2,
                         constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter for main menu",
                         constants.SCREEN_WIDTH / 2,
                         constants.SCREEN_HEIGHT / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    """
    Pause View Class
    On Key Press method -   parameters:
                        key             - key code
                        _modifiers      - modifiers, i.e. shift, ctrl, etc.
                        see arcade docs for details
    Handles key presses in the pause screen
    """
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # main menu
            menu_view = MenuView()
            self.window.show_view(menu_view)
