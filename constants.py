"""
Main Constants
Adjust to change game play

TODO: 1. LAN Game (powerups exchange) <<<<

"""

GAME_MODES = ('2 players', '1 player vs AI', '2 players LAN')

# Window size etc.
SCREEN_WIDTH = 1600                     # Window width in pixels
SCREEN_HEIGHT = 800                     # Window height in pixels
SCREEN_FULLSCREEN = 1                   # Do you want it full screen? Go for it!
SCREEN_TITLE = "Space Duel v2.0"        # Window caption
SPRITE_SIZE = 64

# Spacecraft related
MAX_SPEED = 10.0                        # Maximum speed allowed
MAX_ROTATION_SPEED = 5                  # Rotation angle per keypress
ACCELERATION = 1                        # Acceleration per update cycle
MAX_HEALTH = 200                        # Initial health for both players
BOUNCE_SPEED_RATIO = 0.1                # When bounce from edges reduce speed

# Weapon related
BULLET_SPEED = 20                       # Default laser/bullet speed
BULLET_COOLDOWN = 50                    # Laser cool down cycles. Decrease for rapid fire or collect powerups
HIT_DAMAGE = 10                         # Damage done when laser hits enemy
MAX_MINES = 5                           # Max mines allowed per player
MINE_COOLDOWN = 100                     # Mine cool down cycles
MINE_DAMAGE = 50                        # Damage done by 1 mine to the enemy

# Power-ups related
POWERUP_EFFECT = 10                     # Power up effect on laser cool down
MAX_POWERUPS = 1                        # No of power-ups in the field

# AI related for single player game
AI_EASY_SHOOT_PACE = 150                # AI shoot pace - Difficult EASY
AI_MEDIUM_SHOOT_PACE = 50               # AI shoot pace - Difficult MEDIUM
AI_HARD_SHOOT_PACE = 10                 # AI shoot pace - Difficult HARD
AI_NIGHTMARE_SHOOT_PACE = 1             # AI shoot pace - Difficult NIGHTMARE
AI_SHOOT_PACE = 50                      # AI shoot pace, less number - faster
AI_PREDICTIVE = 0                       # AI predictive aiming - calc where opponent will be in future and shoot there

# Burst related
BURST_PARTICLE_COUNT = 200              # No of particles in an explosion
DEFAULT_PARTICLE_LIFETIME = 1.0         # Particle lifetime
PARTICLE_SPEED_FAST = 1.0               # Particle speed
DEFAULT_SCALE = 0.2                     # Scale of bitmap, 20%
DEFAULT_ALPHA = 32                      # Alpha
MAX_EMITTERS = 2                        # Maximum number of burst emitters on the list per player

# LAN game related
LAN_PORT = 12345                        # Port number used for LAN game
LISTEN_BACKLOG = 2
SOCKET_TIMEOUT = 0.01
MAX_LAN_ERRORS = 5
