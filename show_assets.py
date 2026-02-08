import os
import pygame

from constantes import *

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'images')

pygame.init()
SCREEN = pygame.display.set_mode((LARGEUR_JEU, HAUTEUR_JEU))
pygame.display.set_caption('Assets quick viewer')
clock = pygame.time.Clock()

files = []
for root, dirs, filenames in os.walk(ASSETS_DIR):
    for f in filenames:
        if f.lower().endswith(('.png', '.webp', '.jpg', '.jpeg')):
            files.append(os.path.join(root, f))

if not files:
    print('No image files found in', ASSETS_DIR)
    pygame.quit()
    raise SystemExit

# Load images
images = []
for path in files:
    try:
        img = pygame.image.load(path).convert_alpha()
        images.append((os.path.relpath(path, ASSETS_DIR), img))
    except Exception as e:
        print('Failed to load', path, e)

cols = 4
pad = 8
cell_w = (LARGEUR_JEU - (cols + 1) * pad) // cols
cell_h = cell_w

running = True
index = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                index = (index + 1) % len(images)
            if event.key == pygame.K_LEFT:
                index = (index - 1) % len(images)
            if event.key == pygame.K_ESCAPE:
                running = False

    SCREEN.fill((20, 20, 30))

    # Draw a grid of images around current index
    start = max(0, index - (cols*2))
    display = images[start:start + (cols*2)]
    for i, (name, img) in enumerate(display):
        r = pygame.Rect(pad + (i % cols) * (cell_w + pad), pad + (i // cols) * (cell_h + pad), cell_w, cell_h)
        scaled = pygame.transform.smoothscale(img, (r.w, r.h))
        SCREEN.blit(scaled, r.topleft)
        font = pygame.font.Font(None, 20)
        text = font.render(name, True, (220, 220, 220))
        SCREEN.blit(text, (r.x + 4, r.y + 4))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
