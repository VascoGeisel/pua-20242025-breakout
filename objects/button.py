import pygame

class Button:
    def __init__(self, text, color_text, color_button, x, y, font, screen, display_width, display_height):
        """
        Initializes a button.
        
        Parameters:
        text: The text displayed on the button
        color_text: The color of the text
        color_button: The color of the button background
        x: The horizontal position on the screen (divisor for centering)
        y: The vertical position on the screen (divisor for centering)
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
            self.display_width // self.x - self.text_width // 2,
            self.display_height // self.y - self.text_height // 2,
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
            (self.display_width // self.x - self.text_width // 2,
             self.display_height // self.y - self.text_height // 2)
        )
    
    def is_clicked(self, mouse_pos):
        """
        Checks if the button was clicked.
        
        Parameters:
        mouse_pos: The current mouse position
        return: True if the button was clicked, otherwise False
        """
        return self.button_rect.collidepoint(mouse_pos)