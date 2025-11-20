import time

# Attempt to import a common library used by browser interpreters (like Pyodide/Brython)
try:
    from browser import window, document, html
except ImportError:
    # Fallback for environments without direct browser access
    print("Warning: The 'browser' library (used for canvas access) could not be imported.")
    print("This script is designed to run inside a web-based Python interpreter.")
    # Stop execution if running outside the intended environment
    exit()

# --- Configuration ---
CANVAS_ID = 'game_canvas'
BOX_SIZE = 50
COLOR = 'blue'
SPEED = 2
FPS = 60
FRAME_TIME = 1000 / FPS # milliseconds

# --- State ---
box_x = 50
box_y = 50
direction = 1 # 1 for right, -1 for left
last_time = time.time() * 1000 # Time in milliseconds

# --- Setup Canvas ---
# Check if the canvas element exists in the HTML document
if CANVAS_ID not in document:
    # If not found, create a canvas element and append it to the body (or a specific div)
    canvas = html.CANVAS(id=CANVAS_ID, width=800, height=600, style="border: 2px solid #3b82f6; background-color: #0a0a2a;")
    document <= canvas
else:
    canvas = document[CANVAS_ID]

ctx = canvas.getContext('2d')
width = canvas.width
height = canvas.height

# --- Game Loop Functions ---

def update():
    """Updates the position of the box."""
    global box_x, direction
    
    # Update box position
    box_x += SPEED * direction
    
    # Check for boundaries and reverse direction
    if box_x + BOX_SIZE > width:
        direction = -1
    elif box_x < 0:
        direction = 1

def draw():
    """Clears the canvas and draws the current state."""
    # 1. Clear the canvas (fill background)
    ctx.fillStyle = '#0a0a2a' # Deep space blue background
    ctx.fillRect(0, 0, width, height)
    
    # 2. Draw the box
    ctx.fillStyle = COLOR
    ctx.fillRect(box_x, box_y, BOX_SIZE, BOX_SIZE)
    
    # 3. Draw instructions
    ctx.fillStyle = '#ffffff'
    ctx.font = "20px sans-serif"
    ctx.fillText(f"Running Python Game on Canvas! FPS: {FPS}", 10, 30)

def game_loop(timestamp):
    """The main loop, called by requestAnimationFrame."""
    global last_time
    
    # Calculate delta time (optional, but good practice for smooth motion)
    current_time = timestamp
    delta_time = current_time - last_time
    
    if delta_time >= FRAME_TIME:
        update()
        draw()
        last_time = current_time - (delta_time % FRAME_TIME)

    # Request the next frame from the browser
    window.requestAnimationFrame(game_loop)

# --- Start the Game ---
# Use the browser's requestAnimationFrame for smooth loop
window.requestAnimationFrame(game_loop)

print("Python game loop initialized and running.")