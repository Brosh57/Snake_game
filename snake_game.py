import curses
import random
import time

def main():
    # Initialize curses
    screen = curses.initscr()
    curses.start_color()
    curses.curs_set(0)  # Hide cursor
    curses.noecho()  # Don't echo key presses
    curses.cbreak()  # React to keys instantly without Enter
    screen.keypad(True)  # Enable special keys like arrows
    screen.timeout(100)  # Non-blocking input (refresh rate)
    
    # Setup colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score and messages
    
    # Get screen dimensions
    screen_height, screen_width = screen.getmaxyx()
    
    # Setup game area - slightly smaller than full screen
    game_win = curses.newwin(screen_height-2, screen_width-2, 1, 1)
    game_win.keypad(True)
    game_win.timeout(100)  # Refresh rate
    
    # Game variables
    snake = [[screen_height//2, screen_width//4]]  # Snake starts as a single segment
    direction = curses.KEY_RIGHT  # Initial direction
    
    # Create initial food position
    food = [random.randint(1, screen_height-4), random.randint(1, screen_width-4)]
    game_win.addch(food[0], food[1], 'O', curses.color_pair(2))
    
    score = 0
    
    # Display start instructions
    screen.clear()
    screen.addstr(0, 0, "Snake Game - Use arrow keys to move. Press 'q' to quit", curses.color_pair(3))
    screen.refresh()
    
    # Game loop
    key = curses.KEY_RIGHT  # Initial key
    while key != ord('q'):  # 'q' to quit
        # Get next key press
        next_key = game_win.getch()
        
        # If no key is pressed, continue with current direction
        key = key if next_key == -1 else next_key
        
        # Determine new direction (don't allow 180 degree turns)
        if key == curses.KEY_DOWN and direction != curses.KEY_UP:
            direction = curses.KEY_DOWN
        elif key == curses.KEY_UP and direction != curses.KEY_DOWN:
            direction = curses.KEY_UP
        elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
            direction = curses.KEY_LEFT
        elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
            direction = curses.KEY_RIGHT
        
        # Calculate new head position
        new_head = [snake[0][0], snake[0][1]]
        if direction == curses.KEY_DOWN:
            new_head[0] += 1
        elif direction == curses.KEY_UP:
            new_head[0] -= 1
        elif direction == curses.KEY_LEFT:
            new_head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            new_head[1] += 1
        
        # Insert new head
        snake.insert(0, new_head)
        
        # Check for collisions with border
        if (new_head[0] <= 0 or new_head[0] >= screen_height-3 or 
            new_head[1] <= 0 or new_head[1] >= screen_width-3):
            break
        
        # Check for collisions with self
        if new_head in snake[1:]:
            break
        
        # Check if snake ate the food
        if snake[0] == food:
            # Increment score
            score += 10
            
            # Update score display
            screen.addstr(0, 0, f"Score: {score} - Use arrow keys to move. Press 'q' to quit", curses.color_pair(3))
            screen.refresh()
            
            # Create new food
            food = None
            while food is None:
                new_food = [
                    random.randint(1, screen_height-4),
                    random.randint(1, screen_width-4)
                ]
                # Make sure new food isn't on the snake
                food = new_food if new_food not in snake else None
            
            game_win.addch(food[0], food[1], 'O', curses.color_pair(2))
        else:
            # Remove tail segment
            tail = snake.pop()
            game_win.addch(tail[0], tail[1], ' ')
        
        # Draw snake head
        try:
            game_win.addch(snake[0][0], snake[0][1], '#', curses.color_pair(1))
        except curses.error:
            # Handle potential cursor position errors at screen edges
            pass

    # Game Over
    curses.endwin()
    print(f"Game Over! Your score: {score}")
    time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        curses.endwin()  # Ensure terminal is restored
        print(f"An error occurred: {e}")

