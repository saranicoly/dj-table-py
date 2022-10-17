import os
import pygame
import pygame_menu

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
        onchange=toggle_music,
        args=(i,),
        align=pygame_menu.locals.ALIGN_RIGHT,
    )

menu.add.button("Quit", pygame_menu.events.EXIT)


menu.mainloop(surface)
