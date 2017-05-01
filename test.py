# from app.models import UserProfile
# from werkzeug.security import generate_password_hash, check_password_hash

# users = UserProfile.query.all()
# for user in users:
#     print check_password_hash(user.password, 'JhanelleXCX17')
#     if user.username == 'administrator' and check_password_hash(user.password, 'JhanelleXCX17'):
#         print user.username, user.password
            
import requests
from bs4 import BeautifulSoup
import urlparse

# def getimageurls(url = None):
url = "https://www.google.com.jm/search?q=high+quality+wallpapers&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwiQjPPA4IbTAhXE1CYKHSOnDSgQsAQIFw&biw=1536&bih=744&dpr=1.25#tbm=isch&q=electronics+appliances+hd"
url = 'https://www.amazon.com/Vero-Womens-Dress-Peach-Medium/dp/B01MTA2137/ref=lp_16313218011_1_1?s=apparel&ie=UTF8&qid=1493395294&sr=1-1&nodeID=16313218011&psd=1'
result = requests.get(url)
soup = BeautifulSoup(result.text, "lxml")

# This will look for a meta tag with the og:image property
og_image = (soup.find('meta', property='og:image') or
            soup.find('meta', attrs={'name': 'og:image'}))
if og_image and og_image['content']:
    print og_image['content']
    print ''

# This will look for a link tag with a rel attribute set to 'image_src'
thumbnail_spec = soup.find('link', rel='image_src')
if thumbnail_spec and thumbnail_spec['href']:
    print thumbnail_spec['href']
    print ''

images = []
for img in soup.findAll("img", src=True):
   images += [img["src"]]
   print img["src"]
# return images

print 'done'