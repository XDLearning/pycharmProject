# -*- coding: UTF8 -*-
"""
@Project        ：pycharmProject 
@File           ：220815englishDownload.py
@Author         ：Di Xu
@Date           ：2022/8/15 19:26
@Description    : The project for downloading English videos of senior high school.
"""
import requests
import logging
import re
from os import makedirs
from os.path import exists

# The url of kekenet.basic
BASIC_MP3 = 'http://k6.kekenet.com/'
BASIC_LRC = 'http://www.kekenet.com/'

# the dir of want to download.
RESULTS_DIR = 'resultsEnglishBook2'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# the basic setting of logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


class IndexPage(object):
    def __init__(self, url):
        self.url = url

    def scrape_page(self):
        logging.info('scraping %s...', self.url)
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                return result
            logging.error('get invalid status code %s while scraping %s', response.status_code, self.url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', self.url, exc_info=True)

    def find_url(self):
        content = self.scrape_page()
        pattern_url = re.compile('<a.*?href="(http.*?)".*?title="人教版')
        results = re.findall(pattern_url, content)
        return results

    def find_name(self):
        content = self.scrape_page()
        pattern_title = re.compile('<a.*?href="http.*?".*?title="(人教版.*?)"')
        results = re.findall(pattern_title, content)
        # change title from Chinese to English.
        for i in range(len(results)):
            results[i] = 'Book' + re.sub('[\u4e00-\u9fa5]|\W', '', results[i])
        return results


class Page(IndexPage):
    def __init__(self, name, url):
        super().__init__(url)
        self.name = name
        self.mp3_url = None
        self.lrc_url = None

    def find_mp3(self):
        # get html
        html = super().scrape_page()
        # search url from content
        pattern = re.compile('<audio.*?src="(.*?)".*?id="myaudio"')
        result = re.search(pattern, html)
        if result:
            self.mp3_url = result.group(1)
            logging.info('Found the url of mp3...%s', self.mp3_url)
        else:
            pattern = re.compile('thunder_url.*?(Sound.*?)"')
            result = re.search(pattern, html)
            self.mp3_url = BASIC_MP3 + result.group(1)
            logging.warning('That is another mp3 url...')
        # The result of match is an object
        # <re.Match object; span=(22916, 22972), match='http://k6.kekenet.com/Sound/2016/04/m1u5u_4728742>
        # It is not show all details.

    def find_lrc(self):
        # get html
        html = super().scrape_page()
        # search url from content
        pattern = re.compile('getLrcCon.*?"(.*?)".*?script')
        result = re.search(pattern, html)
        if result:
            self.lrc_url = result.group(1)
            logging.info('Found the url of lrc...%s', self.lrc_url)
        else:
            pattern = re.compile('jmlrc.*?(Sound.*?.lrc)"')
            result = re.search(pattern, html)
            self.lrc_url = BASIC_LRC + result.group(1)
            logging.warning('That is another lrc url...')
        # such self.lrc_url like 'http://www.kekenet.com/Sound/2016/08/929c898dacaa5d54ea91.lrc'

    def load_mp3(self):
        logging.info('loading %s...', self.mp3_url)
        english_mp3 = requests.get(self.mp3_url)
        file_path = f'{RESULTS_DIR}/{self.name}.mp3'
        with open(file_path, 'wb') as f:
            f.write(english_mp3.content)
        logging.info('loaded successfully %s MP3.', file_path)

    def load_lrc(self):
        logging.info('loading %s...', self.lrc_url)
        english_lrc = requests.get(self.lrc_url)
        file_path = f'{RESULTS_DIR}/{self.name}.lrc'
        with open(file_path, 'wb') as f:
            f.write(english_lrc.content)
        logging.info('loaded successfully %s LRC.', self.name)


def main():
    # 0. get page_url,page_name from index url.
    index_url = 'http://www.kekenet.com/gaokao/16160/'
    index_page = IndexPage(index_url)
    page_name = index_page.find_name()
    page_url = index_page.find_url()
    for i in range(len(page_name)):
        item_page = Page(page_name[i], page_url[i])
        try:
            # 1. from page_url to mp3_url, lrc_url
            item_page.find_mp3()
            item_page.find_lrc()
        except AttributeError:
            # 2. lrc_url does not exist, download .mp3
            item_page.load_mp3()
            logging.error('Loading %s.lrc failed...It does not exist.', item_page.name)
        except Exception as f:
            # 3. Some Error such as the Network.
            print(repr(f))
            logging.error('Loading %s.mp3 or lrc failed...Refresh the DNS and try again.', item_page.name)
        else:
            item_page.find_mp3()
            item_page.load_lrc()


if __name__ == '__main__':
    main()
