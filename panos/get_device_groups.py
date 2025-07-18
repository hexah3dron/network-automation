import panorama_api
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import os

load_dotenv()

PANOS_APIKEY = os.getenv('PANOS_APIKEY')
PANOS_USERNAME = os.getenv('PANOS_USERNAME')
PANOS_PASSWORD = os.getenv('PANOS_PASSWORD')
PANOS_HOSTNAME = os.getenv('PANOS_HOSTNAME')

if __name__ == "__main__":
    pano = panorama_api.PanoramaAPI(
        api_key=PANOS_APIKEY,
        host=PANOS_HOSTNAME,
        username=PANOS_USERNAME,
        password=PANOS_PASSWORD
    )

    try:
        # get list of device groups
        xpath = "/config/devices/entry[@name='localhost.localdomain']/device-group"
        response = pano.get_config(xpath)
        print(ET.tostring(response, encoding='unicode'))

    except Exception as e:
        print("Error:", e)
