import json
import requests
import re

i = 0
id_set = set()


def urlencode(i: str) -> str:
    i = i.replace(',', '%2C')
    i = i.replace('/', '%2F')
    i = i.replace(':', '%3A')
    i = i.replace('@', '%40')
    i = i.replace('#', '%23')
    return i


def getItems(filename: str, category: str, num: int = 75, last: int = 0):
    host = 'https://chrome.google.com/webstore/ajax/item?'
    _count = max(0, 0 + (last - 3) * num)
    global i
    j = 0
    allpara = 'hl=zh-CN&gl=US&pv=20200924&' \
              'mce=atf,pii,rtr,rlb,gtc,hcn,svp,wtd,hap,nma,dpb,ar2,rp2,utb,' \
              'hbh,hlb,c3d,ncr,hns,ctm,ac,hot,mac,epb,fcf,rma,pot,evt,hib&' \
              'requestedCounts=infiniteWall:75:0:false' \
              '&token=featured:0@1017917:7:false,mcol#top_picks_photos:0@1017918:9:true,' \
              'infiniteWall:0@1017919:315:false&' \
              'category=ext/28-photos&_reqid=1635460&rt=j'

    if last == 0:
        with open(filename, mode='a+', encoding='utf-8') as f:
            attr = ['id', 'name', 'developer', 'desp', 'cate', 'star', 'comment', 'user', 'url']
            f.write(','.join(attr) + '\n')

    while True:
        j += 1
        print(j)
        _count += 75
        para = 'hl=zh-CN&gl=US&pv=20200924&' \
               'mce=atf,pii,rtr,rlb,gtc,hcn,svp,wtd,hap,nma,dpb,ar2,rp2,utb,' \
               'hbh,hlb,c3d,ncr,hns,ctm,ac,hot,mac,epb,fcf,rma,pot,evt,hib&' \
               f'requestedCounts=infiniteWall:{num}:0:false' \
               '&token=featured:0@1017917:7:false,mcol#top_picks_photos:0@1017918:9:true,' \
               f'infiniteWall:0@1017919:{_count}:false&' \
               f'category=ext/{category}&rt=j'

        data = {'login': '', 'f.req': f'[[["infiniteWall",{num},0,false]],"ext/{category}"]'}
        r = requests.post(host + urlencode(para), data)
        if not r.ok:
            print('NOT OK!', r.reason)
            exit(1)

        to_delete = re.match(r'[\s\S]*?(?=\[)', r.text).group()
        ext_list = json.loads(r.text.replace(to_delete, ''))[0][1][1]

        if not isinstance(ext_list, list):
            break

        if len(ext_list) == 0:
            break

        with open(filename, 'a+', encoding='utf-8') as _f:
            for ext in ext_list:
                values = ['-' for i in range(9)]
                values[0:5] = ext[0] or '-', ext[1] or '-', ext[2] or '-', ext[6] or '-', ext[9] or '-'
                values[5:8] = ext[12] or '-', ext[22] or '-', ext[23] or '-'
                values[8] = ext[37] or '-'

                if values[0] not in id_set:
                    id_set.add(values[0])
                    values = [str(i) for i in values]
                    values = [i.replace('\n', '') for i in values]  # \n
                    values = [i.replace('\r', '') for i in values]  # \r
                    values = [f'"{i}"' if ',' in i else i for i in values]  # comma
                    _f.write(','.join(values) + '\n')
                    i += 1
                else:
                    continue


if __name__ == '__main__':
    cate = '15-by-google'
    filename = cate + '.txt'
    # if error occurs, just note down the last int num
    # printed and add it to current 'last' value to restart
    # from the assigned location
    getItems(filename, cate, last=0)
