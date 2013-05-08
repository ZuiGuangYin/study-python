import re
import urllib2

def extract_links(html):
    blocks = re.findall(r'<ul class=l13>.*?</ul>', html, re.S)
    links = []
    for b in blocks:
        links += re.findall(r'<a href=(\S+)[^<>]*>([^<>]*)</a>', b)
    return links

def extract_content(html):
    m = re.search('<!--\xd5\xfd\xce\xc4\xc4\xda\xc8\xdd\xbf\xaa\xca\xbc-->.*<!--\xd5\xfd\xce\xc4\xc4\xda\xc8\xdd\xbd\xe1\xca\xf8-->', html, re.S)
    return m and html_to_text(m.group()) or ''

def html_to_text(html):
    html = re.sub(r'<p>(.*?)</p>', r'\1\n', html)
    html = re.sub(r'<[^<>]*>', '', html)
    return "\n\n" + html.strip() + "\n\n"

def url_get(url):
    u = urllib2.urlopen(url)
    c = u.read()
    u.close()
    return c

def download_book(urlindex, filename):
    links = extract_links(url_get(urlindex))

    fp = open(filename, 'w')
    for link in links:
        u = 'http://book.sina.com.cn' + link[0]
        title = link[1]
        fp.write(title)
        fp.write(extract_content(url_get(u)))
        #print u
       # print title
    fp.close()

# 使用例子，下载并合成一个单独的 txt
if __name__ == '__main__':
    download_book('http://book.sina.com.cn/nzt/novel/lit/wxdfd/index.shtml', '杜拉拉升职记.txt')
