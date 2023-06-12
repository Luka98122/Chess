import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))


font = pygame.font.Font(None, 32)

input_box = pygame.Rect(100, 100, 232, 32)
color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color = color_inactive
active = False
text = ""
done = False
lines = [""]


def update_text(text, font, box_width):
    words = text.split(" ")
    lines = [""]
    for word in words:
        temp_line = lines[-1] + " " + word if lines[-1] else word
        temp_text = font.render(temp_line, True, color)
        if temp_text.get_width() <= box_width:
            lines[-1] = temp_line
        else:
            lines.append(word)
    return lines


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ""
                    lines = [""]
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                lines = update_text(text, font, input_box.width - 10)

    screen.fill((30, 30, 30))
    for i, line in enumerate(lines):
        txt_surface = font.render(line, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5 + i * 32))
    input_box.h = max(32, len(lines) * 32)
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()

pygame.quit()
