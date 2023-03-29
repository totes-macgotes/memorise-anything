from PIL import Image, ImageDraw, ImageFont

import os


def clear_dir():
    directory = 'static/card_creator'
        
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Fehler beim Löschen der Datei {}: {}'.format(file_path, e))


def create_text_card(text, pair_id, first_of_pair):
    image = Image.new('RGB', (800, 600), color = (210, 210, 210))

    font = ImageFont.truetype("LEMONMILK-Regular.otf", 90)

    draw = ImageDraw.Draw(image)

    textwidth, textheight = draw.textsize(text, font)

    x = (image.width - textwidth) / 2
    y = (image.height - textheight) / 2

    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    filename = ""
    if first_of_pair:
        filename += str(pair_id) + "A"
    else:
        filename += str(pair_id) + "B"
    
    image.save("static/card_creator/" + filename + ".png")

def create_image_card(image_path, pair_id, first_of_pair):
    image = Image.open(image_path)

    image.thumbnail((800, 600), Image.ANTIALIAS)

    filename = ""
    if first_of_pair:
        filename += str(pair_id) + "A"
    else:
        filename += str(pair_id) + "B"
    
    image.save("static/card_creator/" + filename + ".png")