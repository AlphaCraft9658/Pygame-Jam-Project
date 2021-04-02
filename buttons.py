try:
    import pygame
    from pygame.locals import *
except ImportError:
    import os
    try:
        os.system("pip install pygame --user")
        # noinspection PyUnresolvedReferences
        import pygame
        from pygame.locals import *
    except ImportError:
        print("Could not install pygame! Try installing it manually!")
        from time import sleep
        sleep(3)
        exit()
    else:
        print("All libraries successfully installed!")
print("All libraries successfully imported!")


pygame.init()
if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("Pygame Button Test")
    click = pygame.mixer.Sound("aud/sounds/plastic click.wav")
buttons = pygame.sprite.Group()

COLOR = Union[pygame.Color, Tuple[int, int, int], Tuple[int, int, int, int]]
# define class for clickable buttons
class Button(pygame.sprite.Sprite):
    # don't forget to import pygame to use this system yourself
    # pass arguments this way: ((button x, button y, button width, height), (border width, radius), ((button r, g, b),/
    # (button hover r, g, b), (button click r, g, b), (border r, g, b), (border hover r, g, b), (border click r, g, b))/
    # click_sound (valid Sound object)
    # (text, (text r, g, b), size, font), event
    # pass a separate declared function or a lambda for "event" to make it work the way you want
    def __init__(self, surface: pygame.Surface, box: Union[Rect, Tuple[int, int, int, int]] = Rect(0, 0, 100, 50),
                 border: Tuple[int, int] = (5, 5),
                 colors: Tuple[COLOR, COLOR, COLOR, COLOR, COLOR, COLOR] =
                 ((225, 225, 225), (200, 200, 200),
                 (180, 180, 180), (180, 180, 180),
                 (170, 170, 170), (130, 130, 130)),
                 click_sound: pygame.mixer.Sound = None,
                 text: tuple[str, Color] = None,
                 sys_font: pygame.font.SysFont = None,
                 custom_font: pygame.font.Font = None,
                 click_event=(lambda: print("Button Pressed"))):
        super().__init__()
        self.screen = surface
        self.border_width = border[0]
        self.border_radius = border[1]
        self.color = colors[0]
        self.hover_color = colors[1]
        self.click_color = colors[2]
        self.border_color = colors[3]
        self.border_hover_color = colors[4]
        self.border_click_color = colors[5]
        self.click_sound = click_sound
        self.rect = Rect(box[0], box[1], box[2], box[3])
        if text:
            self.text = text[0]
            self.text_color = text[1]
            self.font = None
            self.custom_font = None
            self.default_font = None
            if sys_font:
                self.font = sys_font
            elif custom_font:
                self.custom_font = custom_font
            else:
                self.default_font = pygame.font.SysFont("Arial", (self.rect.width // len(self.text)))
        self.clicked = False
        self.hover = False
        self.click_event = click_event
        buttons.add(self)

        if text:
            if self.font:
                self.text_rendered = self.font.render(self.text, True, self.text_color)
            elif self.custom_font:
                self.text_rendered = self.custom_font.render(self.text, True, self.text_color)
            else:
                self.text_rendered = self.default_font.render(self.text, True, self.text_color)
            self.text_rect = self.text_rendered.get_rect()
            self.text_rect.center = self.rect.center

    def update(self):
        if self.clicked:
            pygame.draw.rect(self.screen, self.click_color, self.rect)
            pygame.draw.rect(self.screen, self.border_click_color, self.rect, self.border_radius)
        elif self.hover:
            pygame.draw.rect(self.screen, self.hover_color, self.rect)
            pygame.draw.rect(self.screen, self.border_hover_color, self.rect, self.border_radius)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_radius)
        if self.text:
            if self.font:
                self.text_rendered = self.font.render(self.text, True, self.text_color)
            elif self.custom_font:
                self.text_rendered = self.custom_font.render(self.text, True, self.text_color)
            else:
                self.text_rendered = self.default_font.render(self.text, True, self.text_color)
            self.text_rect = self.text_rendered.get_rect()
            self.text_rect.center = self.rect.center
            self.screen.blit(self.text_rendered, self.text_rect)


def button_check(ev):
    for b in buttons:
        if b.rect.collidepoint(pygame.mouse.get_pos()):
            b.hover = True
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    b.clicked = True
                    if b.click_sound:
                        b.click_sound.play()
                    else:
                        b.clicked = False
            else:
                b.clicked = False
        else:
            b.hover = False

if __name__ == "__main__":
    button = Button(screen, Rect(500, 250, 200, 100), click_sound=click, text=("Test", Color(0, 0, 0)), custom_font=pygame.font.SysFont("Arial", True, 14))
    button2 = Button(screen, Rect(350, 250, 100, 50), click_sound=click, text=("Test123", Color(0, 0, 0)), custom_font=pygame.font.SysFont("Arial", True, 14), click_event=(lambda: print("Test123")))
    run_b = True
    while run_b:
        for event_b in pygame.event.get():
            if event_b.type == pygame.QUIT:
                run_b = False
            button_check(event_b)

        screen.fill((0, 0, 0))
        buttons.update()
        pygame.display.update()
        pygame.time.Clock().tick(60)
    pygame.quit()
