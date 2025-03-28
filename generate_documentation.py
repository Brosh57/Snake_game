#!/usr/bin/env python3
from fpdf import FPDF
import textwrap
import os

class SnakeGameDocumentation:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("helvetica", size=12)
        self.line_height = 7  # mm
        
        # Define text colors
        self.title_color = (0, 0, 139)  # Dark blue
        self.subtitle_color = (0, 100, 0)  # Dark green
        self.body_color = (0, 0, 0)  # Black
        
        # Create the PDF
        self.create_document()
        
    def create_document(self):
        """Generate the complete PDF document."""
        self.add_title("Snake Game Documentation", size=24)
        self.add_subtitle("Project Overview", size=18)
        self.add_paragraph(
            "This documentation explains the Snake Game implementation in Python using the curses library. "
            "The Snake Game is a classic arcade game where the player controls a snake that grows in length "
            "as it consumes food while avoiding collisions with walls and itself."
        )
        
        self.add_subtitle("Game Mechanics", size=18)
        self.add_paragraph("The game operates on the following principles:")
        self.add_bullet_points([
            "The snake moves continuously in the current direction",
            "Player controls the snake using arrow keys (UP, DOWN, LEFT, RIGHT)",
            "Food appears randomly on the screen",
            "When the snake eats food, it grows longer and the score increases",
            "The game ends if the snake hits a wall or itself",
            "The goal is to achieve the highest possible score"
        ])
        
        self.add_subtitle("Code Structure", size=18)
        self.add_paragraph("The snake game is implemented with the following key components:")
        self.add_code_section(
            "# Key game initialization\n"
            "stdscr = curses.initscr()\n"
            "curses.start_color()\n"
            "curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color\n"
            "curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color\n"
        )
        
        self.add_paragraph("The main game loop handles movement, collision detection, and rendering:")
        self.add_code_section(
            "while True:\n"
            "    # Get user input (non-blocking)\n"
            "    key = stdscr.getch()\n"
            "    \n"
            "    # Update snake direction based on key press\n"
            "    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:\n"
            "        direction = key\n"
            "    \n"
            "    # Move snake in current direction\n"
            "    head_y, head_x = snake[0]\n"
            "    if direction == curses.KEY_UP: head_y -= 1\n"
            "    elif direction == curses.KEY_DOWN: head_y += 1\n"
            "    elif direction == curses.KEY_LEFT: head_x -= 1\n"
            "    elif direction == curses.KEY_RIGHT: head_x += 1\n"
            "    \n"
            "    # Check for collisions\n"
            "    if head_y in [0, height-1] or head_x in [0, width-1] or [head_y, head_x] in snake:\n"
            "        game_over = True\n"
            "        break\n"
        )
        
        self.add_subtitle("Running the Game", size=18)
        self.add_paragraph("To run the Snake Game, follow these steps:")
        self.add_bullet_points([
            "Ensure you have Python installed on your system",
            "Set up a virtual environment: python -m venv venv",
            "Activate the virtual environment:",
            "  - Windows: .\\venv\\Scripts\\activate",
            "  - macOS/Linux: source venv/bin/activate",
            "Install required packages: pip install windows-curses (Windows only)",
            "Run the game: python snake_game.py"
        ])
        
        self.add_subtitle("Controls", size=18)
        self.add_bullet_points([
            "UP ARROW: Move snake upward",
            "DOWN ARROW: Move snake downward",
            "LEFT ARROW: Move snake left",
            "RIGHT ARROW: Move snake right",
            "Q: Quit the game"
        ])
        
        self.add_subtitle("Technical Implementation", size=18)
        self.add_paragraph(
            "The game is implemented using the curses library, which provides terminal control for "
            "character-based applications. The snake is represented as a list of coordinates, with "
            "the head at index 0. Food is placed at random coordinates on the screen."
        )
        
        self.add_paragraph(
            "Collision detection checks if the snake's head coordinates match any wall or body coordinates. "
            "When the snake eats food, a new segment is added to the snake and new food is generated at a "
            "random position."
        )
        
        self.add_subtitle("Conclusion", size=18)
        self.add_paragraph(
            "This Snake Game implementation demonstrates key programming concepts including:"
        )
        self.add_bullet_points([
            "Game loops and timing",
            "User input handling",
            "Collision detection",
            "Dynamic data structures (the growing snake)",
            "Terminal UI using curses",
            "Random element generation"
        ])
        
        # Save the PDF
        output_file = "Snake_Game_Documentation.pdf"
        self.pdf.output(output_file)
        print(f"Documentation saved to {output_file}")
    
    def add_title(self, text, size=20):
        """Add a title to the document."""
        self.pdf.set_font("helvetica", "B", size)
        self.pdf.set_text_color(*self.title_color)
        self.pdf.cell(0, self.line_height * 2, text, align="C")
        self.pdf.ln(self.line_height * 3)
        self.reset_text_settings()
    
    def add_subtitle(self, text, size=16):
        """Add a subtitle to the document."""
        self.pdf.set_font("helvetica", "B", size)
        self.pdf.set_text_color(*self.subtitle_color)
        self.pdf.cell(0, self.line_height, text)
        self.pdf.ln(self.line_height * 1.5)
        self.reset_text_settings()
    
    def add_paragraph(self, text):
        """Add a paragraph to the document."""
        self.pdf.set_font("helvetica", size=12)
        self.pdf.set_text_color(*self.body_color)
        
        # Split text into lines to fit within page width
        lines = textwrap.wrap(text, width=80)
        for line in lines:
            self.pdf.cell(0, self.line_height, line)
            self.pdf.ln(self.line_height)
        
        self.pdf.ln(self.line_height / 2)
    
    def add_bullet_points(self, points):
        """Add a list of bullet points to the document."""
        self.pdf.set_font("helvetica", size=12)
        self.pdf.set_text_color(*self.body_color)
        
        for point in points:
            # Use hyphen instead of Unicode bullet
            bullet_text = f"- {point}"
            
            # Split text into lines to fit within page width (accounting for bullet indent)
            lines = textwrap.wrap(bullet_text, width=78)
            
            # First line includes the bullet
            if lines:
                self.pdf.cell(0, self.line_height, lines[0])
                self.pdf.ln(self.line_height)
                
                # Remaining lines are indented
                for line in lines[1:]:
                    self.pdf.cell(0, self.line_height, f"  {line}")
                    self.pdf.ln(self.line_height)
        
        self.pdf.ln(self.line_height / 2)
    
    def add_code_section(self, code):
        """Add a code section to the document."""
        self.pdf.set_font("courier", size=10)
        
        # Split code into lines
        code_lines = code.split('\n')
        
        # Add each line of code
        for line in code_lines:
            self.pdf.cell(0, self.line_height, f"  {line}")
            self.pdf.ln(self.line_height)
        
        self.pdf.ln(self.line_height)
        self.reset_text_settings()
    
    def reset_text_settings(self):
        """Reset text settings to default."""
        self.pdf.set_font("helvetica", size=12)
        self.pdf.set_text_color(*self.body_color)

if __name__ == "__main__":
    try:
        print("Generating Snake Game documentation...")
        doc = SnakeGameDocumentation()
        print("Documentation generated successfully: Snake_Game_Documentation.pdf")
    except Exception as e:
        print(f"Error generating documentation: {e}")
