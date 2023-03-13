import main
from googleapiclient.discovery import build
def test_main():
    youtube = build('youtube', 'v3', developerKey='ВАШ_АПИ_КЛЮЧ')
    channel = youtube.channels().list(id='UCwEthvsKuX9ZaqvIaGfG3RQ', part='snippet,statistics').execute()
    channel1 = main.UserInformation(channel, 'UCPx7nkXKVp7iOnxANvMm4HQ')
    assert str(channel1) == 'YouTube-Канал: Solid'
    assert str(main.PLVideo('PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD', '9lO06Zxhu88')) == ('Название видео: Как устроена IT-столица мира '
                                                                                      '/ Russian Silicon Valley (English subs) \n'
                                                                                      'Плейлист: Литература')
