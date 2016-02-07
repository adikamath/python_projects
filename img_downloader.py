import os, requests, re
from bs4 import BeautifulSoup

## Check and create a new folder on the desktop to store images
if os.path.exists('/Users/cloudhopper/Desktop/comics'): 
    print 'Directory found'
    comic_direc = '/Users/cloudhopper/Desktop/comics/' # Saving the path of the new directory

else: 
    os.makedirs('/Users/cloudhopper/Desktop/comics')
    print 'Directory created'
    comic_direc = '/Users/cloudhopper/Desktop/comics/' 
    
## Store starting URL of the comic's website
url = 'http://xkcd.com/'
loop_max = 0

## Function for downloading current image
def current_image():
    
    global comic_direc, url, comic_num
    
    img_chunk = requests.get(url)
    img_obj = BeautifulSoup(img_chunk.text)
    img_tags = img_obj.select('div #comic img')
    img_regex = re.compile(r'imgs\.xkcd\.com\/comics\/((\w)+\.png)')
    
    if img_regex.search(str(img_tags[0])) != None:
        img_url = 'http://'+img_regex.search(str(img_tags[0])).group()
        img_name = img_regex.search(str(img_tags[0])).group(1) # Selects only the image name
        img_path = comic_direc+img_name
        img = requests.get(img_url, stream = True)
    
    if os.path.exists(img_path): print 'Image:' +img_name+' already exists!!'
    else:
        with open(img_path, 'wb') as f:
            for chunk in img.iter_content():
                f.write(chunk)
            f.close
            print 'Image:'+img_name+' downloaded'
            
            
## Function for getting url of previous image's page
def previous_image():
    
    global prevImg_tags, prevImg_regex, url, img_found, loop_max
    
    prevImg_chunk = requests.get(url) # html object from the current URL
    prevImg_obj = BeautifulSoup(prevImg_chunk.text)
    prevImg_tags = prevImg_obj.select('li a')
    prevImg_tags = map(str, prevImg_tags) # Converting object to string for searching
    prevImg_regex = re.compile(r'\d\d\d\d')
        
    img_found = prevImg_regex.search(str(prevImg_tags[6]))
    if img_found != None:
        comic_num = img_found.group()
    url = 'http://xkcd.com/'+str(comic_num) # Changing the URL to previous image page
    
    ## Storing the second comic number to initiate looping (done only once)
    if loop_max == 0:
        loop_max = comic_num
    
    
### ************************ Downloading starts here *************************** ###
    
current_image()
previous_image()

for i in range(int(loop_max), 0, -1):
    
    try:
        current_image()
        previous_image()
    
    ## There are some image files that aren't .png, if we encounter an error, we skip to next image
    except:
        print 'Error intercepted, downloading next image'
        previous_image()



    
        
