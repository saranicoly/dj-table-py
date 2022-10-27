import os
import pygame
import pygame_menu
import os, sys
from fcntl import ioctl

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

pygame.init()
pygame.mixer.init()
surface = pygame.display.set_mode((800, 800))

song_list = list()


theme = pygame_menu.themes.THEME_DARK.copy()
bg_image = pygame_menu.baseimage.BaseImage(
    image_path=("dj_bg.jpg"), drawing_mode=pygame_menu.baseimage.IMAGE_MODE_SIMPLE
)
theme.background_color = bg_image


def load_songs():
    for file in os.listdir("songs"):
        if file.endswith(".mp3"):
            song_list.append(f"songs/{file}")
    pygame.mixer.set_num_channels(len(song_list))


def toggle_music(state, args):
    music_number = args[0]
    if state:
        pygame.mixer.Channel(music_number).play(
            pygame.mixer.Sound(song_list[music_number])
        )
    else:
        pygame.mixer.Channel(music_number).stop()

if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("Syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

fd = os.open(sys.argv[1], os.O_RDWR)

def ativa_musica(music_number):
    ioctl(fd, RD_SWITCHES)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    red = int.from_bytes(red, 'little')

    if (red % 4 == 0):
        toggle_music(state=1, args=[music_number])


load_songs()

menu = pygame_menu.Menu("Welcome", 800, 800, theme=theme)

for i in range(len(song_list)):
    menu.add.toggle_switch(
        title=f"{i + 1}",
        slider_thickness=25,
        state_text=("O", "I"),
        switch_height=0.8,
        switch_margin=(12, 0),
        toggleswitch_id=str(i),
        onchange=ativa_musica(i),
        args=(i,),
        align=pygame_menu.locals.ALIGN_RIGHT,
    )

menu.add.button("Quit", pygame_menu.events.EXIT)


menu.mainloop(surface)