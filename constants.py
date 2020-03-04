"""
Main Constants
Adjust to change game play

TO DO LIST:
Gameplay:
TODO: 1. LAN Game
TODO: 2. AI - Predictive shooting? (Difficulty = HARD?)
"""

# Window size etc.
SCREEN_WIDTH = 1600                     # Window width in pixels
SCREEN_HEIGHT = 800                     # Window height in pixels
SCREEN_FULLSCREEN = 1                   # Do you want it full screen? Go for it!
SCREEN_TITLE = "Space Duel v0.0000001"  # Window caption

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
MINE_DAMAGE = 50                        # Damage done by 1 mine to the enemy

# Power-ups related
POWERUP_EFFECT = 10                     # Power up effect on laser cool down
MAX_POWERUPS = 1                        # No of power-ups in the field

# AI related for single player game
AI_SHOOT_PACE = 50                      # AI shoot pace, less number - faster
AI_PREDICTIVE = 1                       # AI predictive aiming - calc where Player will be in future and shoot there

# Burst related
BURST_PARTICLE_COUNT = 500              # No of particles in an explosion
DEFAULT_PARTICLE_LIFETIME = 1.0         # Particle lifetime
PARTICLE_SPEED_FAST = 1.0               # Particle speed
DEFAULT_SCALE = 0.2                     # Scale of bitmap, 20%
DEFAULT_ALPHA = 32                      # Alpha
