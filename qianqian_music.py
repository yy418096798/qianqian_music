import requests
from lxml import etree
import re


def get_url(s):

    data = {
        'songIds': '%s' % s,
        'hq': '0',
        'type': 'm4a,mp3',
        'rate':'',
        'pt': '0',
        'flag': '-1',
        's2p': '-1',
        'prerate': '-1',
        'bwt': '-1',
        'dur': '-1',
        'bat': '-1',
        'bp': '-1',
        'pos': '-1',
        'auto':'-1'
    }
    # print(data)

    url = "http://play.taihe.com/data/music/songlink"

    response = requests.post(url=url, data=data)
    # print(response)
    response.encoding = response.apparent_encoding
    music_infos = response.json()["data"]["songList"]
    # print(music_infos)
    for music_info in music_infos:
        music_name = music_info["songName"]
        music_href = music_info["songLink"]
        # print(music_name, music_href)

        return music_name, music_href
#

def down_music():
    m_list = get_url(s)
    url = m_list[1]

    r = requests.get(url)

    with open(m_list[0] + ".mp3", "wb") as f:
        print("正在下载" + m_list[0] + "……")
        f.write(r.content)

    print("down")


def get_music(name):
    url = f"http://music.taihe.com/search?key={name}"
    r = requests.get(url, headers = headers)
    r.encoding = r.apparent_encoding
    # print(r.text)
    tree = etree.HTML(r.text)
    # print(tree)
    song_list = tree.xpath("//span[@class='song-title']/a/@href")
    name_list = tree.xpath("//span[@class='song-title']/a/@title")
    # print(song_list)
    song_id = []
    for i in song_list:
        s_id = re.findall("song/(\d+)", i, re.S)
        if s_id == []:
            break
        song_id.append(s_id)
    # print(name_list)
    list = []
    for i, j, s in zip(name_list, song_id, range(1, 200)):
        print('【%s】' % s + i)
        list.append(j)
    number = input("请输入需下载歌曲的序号：")
    id = list[int(number) - 1]
    return id

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

    # s = "613960566"
    name = input("请输入歌曲名：")


    s = ''.join(get_music(name))

    down_music()
