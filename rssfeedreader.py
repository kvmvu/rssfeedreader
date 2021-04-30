import xml.etree.ElementTree as et

import requests as requests
import validators


def get_url():
    """get user input for feed url"""
    url = input('Enter the RSS feed URL \n')
    if validators.url(url, public=True):
        print("URL looks valid.")
        return url
    else:
        print("Invalid URL: " + url)


def fetch_xml(url):
    """fetch xml content from the feed URL"""
    response = requests.get(url)
    with open('data/latestfeed.xml', 'wb') as f:
        f.write(response.content)


def parse_xml(xml):
    """fetch and convert feed with with given feed URL"""
    try:
        tree = et.parse(xml)
        root = tree.getroot()
        return root
    except et.ParseError as e:
        print("Error while parsing xml: " + xml + "\n Exception: " + e)


def feed_items(root):
    """extract the title, link and description from the feed URL"""
    feed = []
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text
        feed_item = {'title': title, 'link': link, 'description': description}
        feed.append(feed_item)
    return feed


def display_feed(feed):
    """format and print the results of the extraction"""
    for var in range(len(feed)):
        title, link, desc = feed[var].values()
        print('Title: ' + title + '\nLink: ' + link + '\nDescription: ' + desc + '\n')

    return


def main():
    """putting the different functions together"""
    while True:
        url = get_url()
        if url:
            fetch_xml(url)
            root = parse_xml('data/latestfeed.xml')
            feed = feed_items(root)
            display_feed(feed)
        break


if __name__ == '__main__':
    main()
