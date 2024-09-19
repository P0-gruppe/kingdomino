import pygame

from k_domino import tile_types_str
from components import Button, Grid

from state import StateManager

DISPLAY_SIZE = (1480, 1530)
DISPLAY_MIDDLE = DISPLAY_SIZE[0] / 2

print("Setting up pygame")
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
clock = pygame.time.Clock()

print("Initializing fonts")
font = pygame.font.SysFont("Impact Regular", 200)
btn_font = pygame.font.SysFont("Inter", 100)

print("Initializing StateManager")
state_manager = StateManager("dataset.csv")
n_img = state_manager.board.img_idx

print("Initializing buttons")
next_btn = Button(
    x=1150,
    y=1350,
    width=300,
    height=150,
    text="Next",
    font=btn_font,
    color=0x048011,
    text_color="White",
    border_radius=30,
    callback=state_manager.inc_tile_type,
)
undo_btn = Button(
    x=30,
    y=1350,
    width=300,
    height=150,
    text="Undo",
    font=btn_font,
    color=0xD10000,
    text_color="White",
    border_radius=30,
    callback=state_manager.undo,
)
redo_btn = Button(
    x=350,
    y=1350,
    width=300,
    height=150,
    text="Redo",
    font=btn_font,
    color=0xD10000,
    text_color="White",
    border_radius=30,
    callback=state_manager.redo,
)
btns = [next_btn, undo_btn, redo_btn]

grid_border_size = 5
grid_rect = state_manager.img.get_rect(center=(DISPLAY_MIDDLE, 800))
grid_rect = (
    grid_rect[0] - grid_border_size,
    grid_rect[1] - grid_border_size,
    grid_rect[2] + grid_border_size,
    grid_rect[3] + grid_border_size,
)
grid = Grid(*grid_rect, border_size=5)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in btns:
                btn.check_click(event.pos)

            clicked_tile = grid.get_clicked_tile(event.pos)
            if clicked_tile is not None:
                state_manager.set_tile(clicked_tile, state_manager.current_tile_type)

    screen.fill("white")

    # RENDER YOUR GAME HERE
    text = font.render(
        f"Select {tile_types_str[int(state_manager.current_tile_type)]}s",
        False,
        (0, 0, 0),
    )
    screen.blit(text, text.get_rect(center=(DISPLAY_MIDDLE, 150)))
    screen.blit(
        state_manager.img,
        state_manager.img.get_rect(center=(DISPLAY_MIDDLE, 800)),
    )

    for btn in btns:
        btn.draw(screen)

    grid.draw(screen, state_manager.board.tiles)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
