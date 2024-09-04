from yta_general_utils.tmp_processor import create_tmp_filename
from yta_general_utils.file_downloader import download_image
from PIL import Image, ImageFont, ImageDraw, ImageOps
from random import randrange as random_randrange

import textwrap
import numpy as np

def create_tripadvisor_review_image(review: str = None, avatar_url: str = None, username: str = None, city: str = None, contributions_number: int = random_randrange(30), rating_stars: int = (random_randrange(5) + 1), title: str = None, output_filename: str = None):
    # TODO: This must be set by the user in .env I think
    __FONTS_PATH = 'C:/USERS/DANIA/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/'

    # TODO: Do more checkings please
    # TODO: Check contributions_number is in between 1 and 30 and is a number
    # TODO: Check rating_stars is a number between 1 and 5
    # TODO: Check title exists
    # TODO: Check review exists

    bold_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST_777_BOLD_BT.TTF', 22, encoding = 'unic')
    normal_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST-777-FONT.OTF', 16, encoding = 'unic')
    review_font = ImageFont.truetype(__FONTS_PATH + 'HUMANIST-777-FONT.OTF', 20, encoding = 'unic')

    # Create white review background (440 is h, 800 is w)
    img = np.zeros((440, 800, 3), dtype = np.uint8)
    img.fill(255)
    img = Image.fromarray(img).convert('RGBA')
    draw = ImageDraw.Draw(img)

    # Place avatar image circle at (24, 31)
    image_filename = create_tmp_filename('tmp_avatar.png')
    if not avatar_url:
        avatar_url = 'https://avatar.iran.liara.run/public'
    download_image(avatar_url, image_filename)
    avatar_image = Image.open(image_filename)

    # Make image fit and then mask with circle
    avatar_image = ImageOps.fit(avatar_image, (64, 64))
    mask = Image.new('L', avatar_image.size, 0)
    circle_draw = ImageDraw.Draw(mask)
    circle_draw.ellipse((0, 0, 64, 64), fill = 255)
    result = Image.new('RGBA', avatar_image.size, (255, 255, 255))
    result.paste(avatar_image, (0, 0), mask)

    img.paste(result, (24, 31))

    # I check if I need some fake information
    fake_data = None
    if not username or not city:
        # TODO: Move this below to a 'get_json_from_url' or similar
        # TODO: Create the new 'yta-data-provider' library and include this
        import requests
        response = requests.get('https://fakerapi.it/api/v1/persons?_locale=es_ES')
        data = response.json()
        fake_data = data['data'][0] # First person generated data

    # Put reviewer name at (103, 33)
    if not username:
        username = fake_data['firstname'] + ' ' + fake_data['lastname']
    draw.text((103, 33), username, font = bold_font, fill = (84, 84, 84), line_height = '19px', width = 700)
    
    # Write city and contributions at (103, 65)
    if not city:
        city = fake_data['address']['city']
    # TODO: Check contributions_number is a number
    draw.text((103, 65), city + ' · ' + str(contributions_number) + ' contribuciones', font = normal_font, fill = (84, 84, 84), line_height = '19px', width = 700)

    # Build the evaluation (in green circles) at (24, 126)
    def __draw_filled_ellipse(xy):
        return draw.ellipse(xy, fill = (0, 170, 108), outline = (0, 170, 108))
    def __draw_unfilled_ellipse(xy):
        return draw.ellipse(xy, fill = (255, 255, 255), outline = (0, 170, 108))
    
    x = 24
    for i in range(5):
        if i < rating_stars:
            __draw_filled_ellipse((x, 126, x + 24, 126 + 24))
        else:
            __draw_unfilled_ellipse((x, 126, x + 24, 126 + 24))
        x += 24 + 6

    # Place the review title at (24, 164)
    if not title:
        # TODO: Fake review title with AI
        title = 'Menuda pasada'
    draw.text((24, 164), title, font = bold_font, fill = (84, 84, 84), line_height = '19px')

    # Place the review date at (24, 199)
    # TODO: Implement 'date' parameter
    # TODO: Implement 'visit_type' options
    draw.text((24, 199), "jul 2019 · En pareja", font = normal_font, fill = (84, 84, 84), line_height = '19px')

    # Place the whole wrapped text starting at (24, 440 - 180)
    # See this: (https://gist.github.com/turicas/1455973) to wrap text
    if not review:
        # TODO: Fake review with AI
        review = 'Estuvimos todo el viaje pensando en que ibamos a poder visitar por fin este sitio, y la verdad es que no ha defraudado nada. Lo disfrutamos de principio a fin y la atención fue espectacular. Llevábamos unas espectativas bastante altas pero, sin lugar a dudas, las han superado. Encantados!!'
    lines = textwrap.wrap(review, width = 76)
    y_text = 440 - 180
    for line in lines:
        left, top, right, bottom = review_font.getbbox(line)
        height = bottom - top
        draw.text((24, y_text), line, font = review_font, fill = (84, 84, 84))
        y_text += height + 8

    # Place the number of likes: 700, 50
    #draw.text((700, 50), "3", font = normal_font, fill = (84, 84, 84), line_height = '19px')

    if not output_filename:
        output_filename = create_tmp_filename('tmp_tripadvisor_review.png')
    img.save(output_filename, 'png')

    # TODO: Why not returning the image instead (?)
    return output_filename