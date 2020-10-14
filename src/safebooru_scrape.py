import requests, os, bs4

""" Safebooru Downloader 
Downloads all images available of selected tags from http://safebooru.org/
Author: toashel @ http://github.com/toashel 
"""


def download_image(url, directory):
    '''Save an image from a URL to a new directory.'''
    image = requests.get(url)
    filetype = image.headers['content-type'].split('/')[-1]
    # name = directory + "/" + url.split("?")[1] + "." + filetype
    name = directory + '/' + url.split('/')[-1].split('?')[0]

    file = open(name, 'wb')
    file.write(image.content)
    file.close()


def get_image(url):
    '''Get the image from a url.'''
    imagePage = requests.get(url)
    imageSoup = bs4.BeautifulSoup(imagePage.text)
    image = imageSoup.find(id='image')
    if image is None:
        return None
    else:
        return image.get('src')


def get_image_links(page, url, pagecount):
    '''Get all image links on a page.'''
    print("Getting image links for Page " + str(pagecount) + "...")
    links = page.find_all('a')
    imageLinks = [url + link.get('href') for link in links if not link.find('img') is None]
    return imageLinks


def get_next_page(page, url):
    '''Get the next page. Returns None if it is the last page.'''
    nextSoup = page.find('a', alt="next")
    if nextSoup is None:
        return None
    else:
        nextUrl = url + 'index.php' + nextSoup.get('href')
    return requests.get(nextUrl)


def main():
    url = 'http://safebooru.org/'

    # userSearch = input("What tags are you searching for?\nEnter them all separated by spaces!\n\n")
    userSearch = 'solo+standing+1girl'
    userURL = url+'index.php?page=post&s=list&tags=' + userSearch

    path = "../dataset/safebooru_images/" + userSearch
    os.makedirs(path, exist_ok=True)  # store images in a directory named after search

    imagescount = 0
    pagecount = 2148
    res = requests.get(userURL)  # page 1

    image_cnt=0

    if "Nothing found" in res.text:
        print("No images found, check your tags?")
        return

    while True:

        soup = bs4.BeautifulSoup(res.text)

        imageLinks = get_image_links(soup, url, pagecount)  # array of links to images
        imagescount += len(imageLinks)

        print("Getting images, this might take a while...")
        images = [get_image(link) for link in imageLinks]  # array of image links

        for i in range(images.count(None)):
            images.remove(None)

        for imageLink in images:
            # imageLink='http:'+imageLink
            print("Downloading image: " + str(imageLink))
            download_image(imageLink, path)
            print("Done!")
            image_cnt+=1
            if image_cnt>=200000:
                exit()

        # Next Page
        res = get_next_page(soup, url)
        if res == None:
            print("Finished! Downloaded " + str(imagescount) + " images!")
            break
        f=open('../log/safebooru_scrape_log.txt','a')
        print(pagecount,file=f)
        pagecount += 1


if __name__ == "__main__":
    main()