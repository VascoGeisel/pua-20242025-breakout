import pygame

class Button:
    def __init__(self, text, color_text, color_button, x, y, x_button, y_button, font, screen, display_width, display_height):
        """
        Initializes a button.
        
        Parameters:
        text: The text displayed on the button
        color_text: The color of the text
        color_button: The color of the button background
        x: The horizontal position on the screen (divisor for centering)
        y: The vertical position on the screen (divisor for centering)
        x_button: The horizontal transposition after seting the corner of the button (divisor for centering, 2 if not at the side or corner of the screen)
        y_button: The horizontal transposition after seting the corner of the button (divisor for centering, 2 if not at the side or corner of the screen)
        font: The font used for the text
        screen: The pygame display surface
        display_width: The width of the display
        display_height: The height of the display
        """
        self.text = text
        self.color_text = color_text
        self.color_button = color_button
        self.x = x
        self.y = y
        self.x_button = x_button
        self.y_button = y_button
        self.font = font
        self.screen = screen
        self.display_width = display_width
        self.display_height = display_height
        
        # Render the text
        self.text_surface = self.font.render(self.text, True, self.color_text)
        
        # Calculate position and size
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
        self.button_rect = pygame.Rect(
            self.display_width // self.x - self.text_width // self.x_button,
            self.display_height // self.y - self.text_height // self.y_button,
            self.text_width,
            self.text_height
        )
    
    def draw(self):
        """
        Draws the button on the screen.
        """
        # Draw the rectangle
        pygame.draw.rect(self.screen, self.color_button, self.button_rect)
        # Draw the text
        self.screen.blit(
            self.text_surface,
            (self.display_width // self.x - self.text_width // self.x_button,
             self.display_height // self.y - self.text_height // self.y_button)
        )
    
    def is_clicked(self, mouse_pos):
        """
        Checks if the button was clicked.
        
        Parameters:
        mouse_pos: The current mouse position
        return: True if the button was clicked, otherwise False
        """
        return self.button_rect.collidepoint(mouse_pos)