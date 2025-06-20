# data.py
import geocoder

# Look up tables
clean_up_query =['my', 'jarvis', 'can you', 'hey', 'please', 'for', 'me', 'tell', 'what is']

# Paths
chrome_path = "chromium"

# LUTs
emails = {
    "sameera official" : "sameerajsharma.ec19@rvce.edu.in",
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
    
