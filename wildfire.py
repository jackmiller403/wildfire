import urllib2
from bs4 import BeautifulSoup
from multiprocessing import Process

SAVE_PATH = '/dir/to/save/photos/'

def downloadWallpaper():
    photoOfTheDay = Process(target=downloadPhotoOfTheDay)
    photoOfTheDay.start()
    weeklyWrapper = Process(target=downloadWeeklyWrapper)
    weeklyWrapper.start()


def downloadPhotoOfTheDay(url="http://photography.nationalgeographic.com/photography/photo-of-the-day/", downloadDays=-1, savePath=SAVE_PATH):
    """downloads the Photo of the Day from National Geogrphics website.
    
    @param downloadDays How many days back to download the photo of the day
    @param savePath The location to save all the wallpaper 
    
    """
    doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(doc)
    wallpaperURL = soup.findAll('div', attrs={'class': 'download_link'}, limit=1)
    
    if len(list(wallpaperURL)):
        wallpaperURL = wallpaperURL[0].findAll('a', limit=1)[0].get('href')
        
        saveURLinDir(wallpaperURL, savePath)
        if downloadDays != -1:
            downloadDays = downloadDays - 1
        print wallpaperURL
    
    previousPhotoURL = None
    if downloadDays >= 1 or downloadDays == -1:
        previousPhotoURL = soup.findAll('p', attrs={'class': 'prev first'}, limit=1)
        if len(list(previousPhotoURL)):
            previousPhotoURL = "http://photography.nationalgeographic.com" + str(previousPhotoURL[0].findAll('a', limit=1)[0].get('href'))
        else:
            previousPhotoURL = "http://photography.nationalgeographic.com" + soup.findAll('p', attrs={'class': 'prev '}, limit=1)[0].findAll('a', limit=1)[0].get('href')

        downloadPhotoOfTheDay(url=previousPhotoURL, downloadDays=downloadDays)


def downloadWeeklyWrapper(savePath=SAVE_PATH):
    """Downloads each gallery from National Geographic's Weekly Wrapper gallery.
     
    @param savePath - the path to save the photos"""
    doc = urllib2.urlopen("http://ngm.nationalgeographic.com/your-shot/weekly-wrapper").read()
    soup = BeautifulSoup(doc)
    galleries = soup.findAll(id="gallerylist", limit=1)[0].findAll('option')
    for gallery in galleries:
        galleryURL = "http://ngm.nationalgeographic.com%s" % str(gallery.get('value'))
        doc = urllib2.urlopen(galleryURL).read()
        soup = BeautifulSoup(doc, 'xml')
        for imageURL in soup.findAll('wallpaper'):
            url = "http://ngm.nationalgeographic.com%s" % imageURL.contents[0].strip()
            saveURLinDir(url, savePath)
            print url

def saveURLinDir(url, dir, downloadIfExists=False):
    """Downloads and saves a file to a folder.
    
    @param url - url path to the file
    @param dir - location to save the file
    @param downloadIfExists - should the file be downloaded if it exists?"""
    if list(dir)[-1] == '/':
        path = str(dir) + str(url.split('/')[-1])
    else:
        path = str(dir) + '/' + str(url.split('/')[-1])
    
    if fileExists(path) and downloadIfExists == False:
        pass
    else:
        f = open(path, 'wb')
        data = urllib2.urlopen(url).read()
        f.write(data)
        f.close()

def fileExists(path):
    """Checks if a file exists and returns a boolean.
    
    @param path The path to the file."""
    try:
       with open(path) as f: return True
    except IOError as e:
       return False

if __name__ == '__main__':
    downloadWallpaper()