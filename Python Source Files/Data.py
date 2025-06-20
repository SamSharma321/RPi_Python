# data.py
import geocoder

# Look up tables
clean_up_query =['will you do me', 'can you do me', 'can you', 'will you', 'do me', 'a', 'and', 'my', 'jarvis', 'hey', 'please', 'for', 'me', 'tell', 'what is', 'favour']

# Paths
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# LUTs
emails = {
    "sameera official" : "ssharma818@gatech.edu",
    "sameera unofficial" : "sharmasameera91@gmail.com",
    "roopa" : "ysjtsha@gmail.com",
    "rupa" : "ysjtsha@gmail.com",
    "jayathirtha" : "ysjayathirtha@gmail.com" # TODO any other emails to be added?
    }

def get_curr_location():
	# use geocoder to get current location
    g = geocoder.ip('me')
    if g.ok:
        return (str(g.city) + ", " + str(g.country))
    else:
        return None
    
