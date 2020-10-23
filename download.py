import pandas as pd
from os import listdir, mkdir
from subprocess import call
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlretrieve

IDM = r'E:\Small Apps\Internet Download Manager\IDMan.exe'
VERSION = '70.0.3538'

if __name__ == '__main__':
    # the folder containing the xlsx files
    folder = 'xlsx'
    # the download path
    dpath = r'F:\craw\EXTs'
    for xlsx in listdir(folder):
        file = f'{folder}/{xlsx}'
        out_folder = xlsx.split('.')[0]
        if not Path(rf'{dpath}\{out_folder}').is_dir():
            mkdir(rf'{dpath}\{out_folder}')
        f = pd.read_excel(file)
        i = total = len(f.index.values)
        print(f'Reading {file}. Items: {total}')
        ids = f.iloc[:, 0].values
        for _id in ids:
            if _id == 'id':
                continue
            if Path(rf'{dpath}\{out_folder}\{_id}.crx').is_file():
                i -= 1
                print(f'{_id} Downloaded. Skip. {i} left.')
            else:
                url = 'https://clients2.google.com/service/update2/crx?' \
                      'response=redirect&os=win&arch=x64&os_arch=x86_64&' \
                      'nacl_arch=x86-64&prod=chromecrx&prodchannel=&' \
                      f'prodversion={VERSION}&lang=zh-CN&' \
                      f'acceptformat=crx3&x=id%3D{_id}%26installsource%3Dondemand%26uc'

                # call([IDM, '/d', url, '/p', rf'F:\craw\EXTs\{out_folder}', '/f', f'{_id}.crx', '/n', '/a'])

                try:
                    urlretrieve(url, rf'{dpath}\{out_folder}\{_id}.crx')
                except HTTPError as e:
                    if e.errno == 401:
                        i -= 1
                        print('Not Free. Skip.', i, 'left.')
                i -= 1
                print('CRX file:', _id, 'Downloaded.', i, 'left.')
