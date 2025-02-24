import pygame

pygame.init()  # Initialize pygame

# Set the screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algorithm Analyzer Tool")

# Load preset fonts
base_font = pygame.font.Font(None, 32)

# Variables for text boxes
min_text = ''
max_text = ''
num_text = ''
MIN_TEXT_DISPLAY = "Min Value:"
MAX_TEXT_DISPLAY = "Max Value:"
NUM_TEXT_DISPLAY = "Number of Elements:"
color_active = pygame.Color('green')
color_passive = pygame.Color('red')
min_active = False
max_active = False
num_active = False 

# Allocate the space for each text box and the boxes that describe them
min_rect = pygame.Rect(245, 125, 75, 32)
min_text_rect = pygame.Rect(min_rect.x - (min_rect.width + 44), min_rect.y, 117, 32)
max_rect = pygame.Rect(450, 125, 75, 32)
max_text_rect = pygame.Rect(max_rect.x - (max_rect.width + 53), max_rect.y, 127, 32)
num_rect = pygame.Rect(350, 175, 75, 32)
num_text_rect = pygame.Rect(num_rect.x - (num_rect.width + 159), num_rect.y, 232, 32)  
random_rect = pygame.Rect(100, 100, 450, 500)
display_rect = pygame.Rect(118, 225, 410, 32)  

run = True
while run:  # Game loop
    for event in pygame.event.get():  # Event handler
        if event.type == pygame.QUIT:  # Handles when you push the X on the window to close the application
            run = False
        
        if event.type == pygame.KEYDOWN: 
            if min_active:
                if event.key == pygame.K_BACKSPACE:  # Checks for backspaces
                    min_text = min_text[:-1]
                elif len(min_text) <= 4 and event.unicode.isdigit():  # Sets character limit and only allows digits to be entered
                    min_text += event.unicode
            
            if max_active:
                if event.key == pygame.K_BACKSPACE:  # Checks for backspaces
                    max_text = max_text[:-1]
                elif len(max_text) <= 4 and event.unicode.isdigit():  # Sets character limit and only allows digits to be entered
                    max_text += event.unicode
            
            if num_active:
                if event.key == pygame.K_BACKSPACE:  # Checks for backspaces
                    num_text = num_text[:-1]
                elif len(num_text) <= 4 and event.unicode.isdigit():  # Sets character limit and only allows digits to be entered
                    num_text += event.unicode
        
        # Checks for which box is clicked on and changes the flags accordingly
        if event.type == pygame.MOUSEBUTTONDOWN:
            if min_rect.collidepoint(event.pos):
                min_active = True
                max_active = False
                num_active = False
            elif max_rect.collidepoint(event.pos):
                max_active = True
                min_active = False
                num_active = False
            elif num_rect.collidepoint(event.pos):
                num_active = True
                min_active = False
                max_active = False
            else:
                min_active = False
                max_active = False
                num_active = False
    
    screen.fill((0, 0, 0)) 
    
    # Draws the rectangles with the desired colors
    pygame.draw.rect(screen, color_active if max_active else color_passive, max_rect, 2)
    pygame.draw.rect(screen, color_active if min_active else color_passive, min_rect, 2)
    pygame.draw.rect(screen, color_active if num_active else color_passive, num_rect, 2)
    pygame.draw.rect(screen, (0, 0, 255), random_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), display_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), max_text_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), min_text_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), num_text_rect, 2)
    
    # Renders the boxes with their text
    min_surface = base_font.render(min_text, True, (255, 255, 255))
    min_surface_text = base_font.render(MIN_TEXT_DISPLAY, True, (255, 255, 255))
    max_surface = base_font.render(max_text, True, (255, 255, 255))
    max_surface_text = base_font.render(MAX_TEXT_DISPLAY, True, (255, 255, 255))
    num_surface = base_font.render(num_text, True, (255, 255, 255))
    num_surface_text = base_font.render(NUM_TEXT_DISPLAY, True, (255, 255, 255))
    
    # Populates the boxes with the texts
    screen.blit(min_surface, (min_rect.x + 5, min_rect.y + 5))
    screen.blit(min_surface_text, (min_text_rect.x + 5, min_text_rect.y + 5))
    screen.blit(max_surface, (max_rect.x + 5, max_rect.y + 5))
    screen.blit(max_surface_text, (max_text_rect.x + 5, max_text_rect.y + 5))
    screen.blit(num_surface, (num_rect.x + 5, num_rect.y + 5))
    screen.blit(num_surface_text, (num_text_rect.x + 5, num_text_rect.y + 5))
    
    pygame.display.update()  # Refreshes the screen

pygame.quit()  # Closes application
