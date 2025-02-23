import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algorithm Analyzer Tool")
base_font = pygame.font.Font(None, 32)

min_text = ''
max_text = ''
num_text = ''

max_rect = pygame.Rect(400, 125, 75, 32)
min_rect = pygame.Rect(225, 125, 75, 32)
num_rect = pygame.Rect(312, 175, 75, 32)  # New box in the middle, 30 pixels below
random_rect = pygame.Rect(200, 100, 300, 500)

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
                else:
                    min_text += event.unicode
            
            if max_active:
                if event.key == pygame.K_BACKSPACE:
                    max_text = max_text[:-1]
                else:
                    max_text += event.unicode
            
            if num_active:
                if event.key == pygame.K_BACKSPACE:
                    num_text = num_text[:-1]
                else:
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
    
    min_surface = base_font.render(min_text, True, (255, 255, 255))
    max_surface = base_font.render(max_text, True, (255, 255, 255))
    num_surface = base_font.render(num_text, True, (255, 255, 255))
    
    screen.blit(min_surface, (min_rect.x + 5, min_rect.y + 5))
    screen.blit(max_surface, (max_rect.x + 5, max_rect.y + 5))
    screen.blit(num_surface, (num_rect.x + 5, num_rect.y + 5))
    
    pygame.display.update()

pygame.quit()
