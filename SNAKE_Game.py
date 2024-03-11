import tkinter
import random  

ROWS = 25
COLS = 25
TILE_SIZE = 25
SNAKE_SPEED = 300  

WINDOW_WIDTH = TILE_SIZE * COLS 
WINDOW_HEIGHT = TILE_SIZE * ROWS 

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()


window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))


window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] 
game_over = False
score = 0
current_speed = SNAKE_SPEED 
prompt_window = None  

def start_game():
    global snake, food, velocityX, velocityY, snake_body, game_over, score, current_speed
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) 
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = [] 
    game_over = False
    score = 0
    current_speed = SNAKE_SPEED 
    window.after(current_speed, draw)

def prompt_play_again():
    global prompt_window
   
    if prompt_window:
        return
    
    prompt_window = tkinter.Toplevel(window)
    prompt_window.title("Play Again?")
    prompt_window.geometry("250x120+400+300")  

    
    prompt_label = tkinter.Label(prompt_window, text="Do you want to play again?", font=("Arial", 12, "bold"), fg="red")
    prompt_label.pack()

   
    yes_button = tkinter.Button(prompt_window, text="Yes", font=("Arial", 12, "bold"), fg="red", command=on_yes_click)
    yes_button.pack(pady=5)

   
    no_button = tkinter.Button(prompt_window, text="No", font=("Arial", 12, "bold"), fg="red", command=on_no_click)
    no_button.pack(pady=5)

def on_yes_click():
    global prompt_window
    
    prompt_window.destroy()
    prompt_window = None
    
    start_game()

def on_no_click():
    global prompt_window
    
    prompt_window.destroy()
    prompt_window = None
    
    window.destroy()

def change_direction(e): 
    global velocityX, velocityY, game_over
    if not game_over:
        if (e.keysym == "Up" and velocityY != 1):
            velocityX = 0
            velocityY = -1
        elif (e.keysym == "Down" and velocityY != -1):
            velocityX = 0
            velocityY = 1
        elif (e.keysym == "Left" and velocityX != 1):
            velocityX = -1
            velocityY = 0
        elif (e.keysym == "Right" and velocityX != -1):
            velocityX = 1
            velocityY = 0
    elif e.keysym in ["Up", "Down", "Left", "Right", "Return"]:  
        start_game()

def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        
        prompt_play_again()
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
    
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    
    canvas.create_oval(food.x + 3, food.y + 5, food.x + TILE_SIZE - 3, food.y + TILE_SIZE - 5, fill='red')

    
    canvas.create_rectangle(snake.x - 5, snake.y - 5, snake.x + TILE_SIZE + 5, snake.y + TILE_SIZE + 5, fill='lime green')

   
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(current_speed, draw)

start_game()  
window.bind("<KeyRelease>", change_direction) 
window.mainloop()
