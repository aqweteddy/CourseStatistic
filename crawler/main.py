import os


def main():
    # print(1)
    # os.system('scrapy crawl ptt -a board=EZSoft -a pages=2')
    os.system('scrapy crawl ptt -a board=Gossiping -a pages=100')
    os.system('scrapy crawl ptt -a board=WomenTalk -a pages=100')
    os.system('scrapy crawl ptt -a board=Baseball -a pages=100')
    os.system('scrapy crawl ptt -a board=HatePolitics -a pages=100')
    # os.system('scrapy crawl ptt -a board=C_Chat -a pages=100')


if __name__ == '__main__':
    main()
