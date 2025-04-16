from sticker2gif import Maker


url = input('URL: ')
tool = Maker(url, log=True)
tool.run()