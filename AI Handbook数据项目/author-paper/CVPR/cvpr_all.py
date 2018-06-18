import requests
from lxml import html

# url = 'https://aaai.org/Library/AAAI/aaai17contents.php'
urls = ['http://openaccess.thecvf.com/CVPR' + str(i) + '.py' for i in range(2013, 2018)]

def main(urls, fileformat='json'):
	fnames = ['cvpr' + str(i) for i in range(13, 18)]
	read_multiple(fnames, urls, fileformat)

def read_multiple(fnames, urls, fileformat='json'):
	for i, url in enumerate(urls):
		with open(fnames[i], 'wb') as fp:
			read_single(fp, url, fileformat)

def read_single(fp, url, fileformat='json'):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(r.status_code)

    root = html.fromstring(r.text)
    content = root.xpath('//dt[@class="ptitle"]')

    _skip = True
    _field = ''
	if fileformat == 'csv':
		towrite = '|'.join((
			unicode(('name')),
			unicode(('title')),
			unicode(('author_total')),
			unicode(('author_order'))
			))+'\n'
		fp.write(towrite.encode('utf-8'))

    for tag in content:
        a = tag.find('a')
        rr = requests.get('http://openaccess.thecvf.com/' + a.get('href'))
        if rr.status_code != 200:
            continue
        tree = html.fromstring(rr.text)

        try:
            kw = tree.xpath('//meta[@name="keywords"]')[0].get('content')
        except Exception as e:
            kw = None

        title = ''
        name = ''
        names = []
        for el in tree.xpath('//meta[contains(@name, "citation_")]'):
            if el.get('name') == 'citation_title':
                title = el.get('content')
            elif el.get('name') == 'citation_author':
                name = el.get('content')
                names.append(name)

        for i, name in enumerate(names):
            u = {
                'name': name.strip(),
                'title': title,
                'keywords': kw,
                'author_total': len(names),
                'author_order': i+1
            }

            if fileformat == 'json':
                fp.write(json.dumps(u)+'\n')
            if fileformat == 'csv':
				towrite = '|'.join((
                    unicode(u.get('name')),
                    unicode(u.get('title')),
                    unicode(u.get('author_total')),
                    unicode(u.get('author_order'))
                    ))+'\n'
                fp.write(towrite.encode('utf-8'))

if __name__ == '__main__':
	import codecs
	main(urls, 'csv')
