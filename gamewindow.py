import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algorithm Analyzer Tool")
base_font = pygame.font.Font(None, 32)
display_font = pygame.font.Font(None,16)

min_text = ''
max_text = ''
num_text = ''

max_rect = pygame.Rect(450, 125, 75, 32)
min_rect = pygame.Rect(245, 125, 75, 32)
num_rect = pygame.Rect(350, 175, 75, 32)  # New box in the middle, 30 pixels below
random_rect = pygame.Rect(100, 100, 450, 500)
display_rect = pygame.Rect(118, 225, 410, 32)  # Long rectangle 50 pixels below num_rect

# Additional text boxes next to main rectangles
max_text_rect = pygame.Rect(max_rect.x - (max_rect.width + 45), max_rect.y, 117, 32)
min_text_rect = pygame.Rect(min_rect.x - (min_rect.width + 53), min_rect.y, 127, 32)
num_text_rect = pygame.Rect(num_rect.x - (num_rect.width + 159), num_rect.y, 232, 32)

MAX_TEXT_DISPLAY = "Min Value:"
MIN_TEXT_DISPLAY = "Max Value:"
NUM_TEXT_DISPLAY = "number of Elements:"

color_active = pygame.Color('green')
color_passive = pygame.Color('red')

min_active = False
max_active = False
num_active = False 

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if min_active:
                if event.key == pygame.K_BACKSPACE:
                    min_text = min_text[:-1]
                elif len(min_text) <= 4 and event.unicode.isdigit():
                    min_text += event.unicode
            
            if max_active:
                if event.key == pygame.K_BACKSPACE:
                    max_text = max_text[:-1]
                elif len(max_text) <= 4 and event.unicode.isdigit():
                    max_text += event.unicode
            
            if num_active:
                if event.key == pygame.K_BACKSPACE:
                    num_text = num_text[:-1]
                elif len(num_text) <= 4 and event.unicode.isdigit():
                    num_text += event.unicode
        
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
    
    pygame.draw.rect(screen, color_active if max_active else color_passive, max_rect, 2)
    pygame.draw.rect(screen, color_active if min_active else color_passive, min_rect, 2)
    pygame.draw.rect(screen, color_active if num_active else color_passive, num_rect, 2)
    pygame.draw.rect(screen, (0, 0, 255), random_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), display_rect, 2)  # Draw the long rectangle
    
    pygame.draw.rect(screen, (255, 255, 255), max_text_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), min_text_rect, 2)
    pygame.draw.rect(screen, (255, 255, 255), num_text_rect, 2)
    
    min_surface = base_font.render(min_text, True, (255, 255, 255))
    min_surface_text = base_font.render(MIN_TEXT_DISPLAY,True,(255, 255, 255))
    max_surface = base_font.render(max_text, True, (255, 255, 255))
    max_surface_text = base_font.render(MAX_TEXT_DISPLAY,True,(255, 255, 255))
    num_surface = base_font.render(num_text, True, (255, 255, 255))
    num_surface_text = base_font.render(NUM_TEXT_DISPLAY,True, (255, 255, 255))
    
    screen.blit(min_surface, (min_rect.x + 5, min_rect.y + 5))
    screen.blit(min_surface_text,(min_text_rect.x + 5,min_text_rect.y + 5))
    screen.blit(max_surface, (max_rect.x + 5, max_rect.y + 5))
    screen.blit(max_surface_text,(max_text_rect.x + 5,max_text_rect.y + 5))
    screen.blit(num_surface, (num_rect.x + 5, num_rect.y + 5))
    screen.blit(num_surface_text,(num_text_rect.x + 5,num_text_rect.y + 5))
    
    pygame.display.update()

pygame.quit()
