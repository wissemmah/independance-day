import os
import pygame

PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
paths = {
    'fond.png': os.path.join(PROJ_ROOT, 'assets', 'images', 'fond.png'),
    'falling.webp': os.path.join(PROJ_ROOT, 'assets', 'images', 'falling.webp'),
    'fond_usa.png (expected by charger_fond_menu)': os.path.join(PROJ_ROOT, 'assets', 'fond_usa.png'),
    'fond_usa_in_images': os.path.join(PROJ_ROOT, 'assets', 'images', 'fond_usa.png')
}

print('Project root:', PROJ_ROOT)
for name, p in paths.items():
    print(f"Exists {name}:", os.path.exists(p), '->', p)

# Try loading with pygame
pygame.init()
for name, p in paths.items():
    if os.path.exists(p):
        try:
            img = pygame.image.load(p)
            print('Loaded', name, 'size', img.get_size())
        except Exception as e:
            print('Failed to load', name, 'error:', e)
    else:
        print('Skipping load (not exists):', name)
pygame.quit()
