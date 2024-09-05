from yta_general_utils.web.scrapper.chrome_scrapper import ChromeScrapper
from yta_general_utils.tmp_processor import create_tmp_filename
from selenium.webdriver.common.by import By
from PIL import Image
from random import randrange
from typing import Union

class YoutubeImageGenerator:
    def create_youtube_comment_image(self, author: str, avatar_url: str, time: str, message: str, likes_number: int, output_filename: Union[str, None] = None):
        """
        This method generates a Youtube comment image with the provided
        information. It will return the image read with PIL, but will
        also store the screenshot (as this is necessary while processing)
        with the provided 'output_filename' if provided, or with as a
        temporary file if not.
        """
        if not author:
            # TODO: Fake author name (start with @)
            pass

        if not avatar_url:
            # TODO: Fake avatar_url or just let the one existing
            pass

        if not time:
            # TODO: Fake time ('hace X años,meses,dias,horas')
            pass

        if not message:
            # TODO: Fake a message with AI
            pass

        if not likes_number:
            likes_number = randrange(50)

        scrapper = ChromeScrapper(False)
        # We go to this specific video with comments available
        scrapper.go_to_web_and_wait_util_loaded('https://www.youtube.com/watch?v=OvUj2WsADjI')
        # We need to scroll down to let the comments load
        # TODO: This can be better, think about a more specific strategy
        # about scrolling
        scrapper.scroll_down(1000)
        scrapper.wait(1)
        scrapper.scroll_down(1000)
        scrapper.wait(1)

        # We need to make sure the comments are load
        scrapper.find_element_by_element_type_waiting('ytd-comment-thread-renderer')
        comments = scrapper.find_elements_by_element_type('ytd-comment-thread-renderer')

        comment = comments[3]
        body = comment.find_element(By.ID, 'body')

        # Change user (avatar) image
        imagen = body.find_element(By.ID, 'img')
        scrapper.set_element_attribute(imagen, 'src', avatar_url)

        # Change date
        time_element = body.find_element(By.ID, 'published-time-text')
        time_element = scrapper.find_elements_by_element_type('a', time_element)[0]
        scrapper.set_element_inner_text(time_element, time)

        # Change user name
        author_element = body.find_element(By.ID, 'header-author')
        author_element = scrapper.find_elements_by_element_type('h3', author_element)[0]
        author_element = scrapper.find_elements_by_element_type('a', author_element)[0]
        author_element = scrapper.find_elements_by_element_type('span', author_element)[0]
        scrapper.set_element_inner_text(author_element, author)

        # Change message
        message_element = scrapper.find_elements_by_id('content-text', comment)[0]
        message_element = scrapper.find_elements_by_element_type('span', message_element)[0]
        scrapper.set_element_inner_text(message_element, message)

        # Change number of likes
        likes_element = scrapper.find_elements_by_id('vote-count-middle', comment)[0]
        scrapper.set_element_inner_text(likes_element, str(likes_number))
        
        scrapper.scroll_to_element(comment)
        
        filename = output_filename
        if not filename:
            filename = create_tmp_filename('tmp_comment_screenshot.png')
        
        scrapper.screenshot_element(comment, filename)

        return Image.open(filename)