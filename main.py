import time
import random
import schedule

import requests
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.account import UpdateProfileRequest

import config

names = []
with open("./names.txt", "r") as names_file:
    names = names_file.read().split('\n')
    names_file.close()

def main():
    with TelegramClient(config.session_name, config.api_id, config.api_hash) as client:
        def job():
            # Get the picture
            response = requests.get(url='https://thispersondoesnotexist.com/image')
            with open('image.jpg', 'wb') as img:
                img.write(response.content)
            print("Changing profile picture... ", end="")
            client(UploadProfilePhotoRequest(
                file=client.upload_file('image.jpg')
            ))
            client(DeletePhotosRequest([client.get_profile_photos('me')[1]]))
            print("Done!")

            # Set the name
            print("Changing profile name... ", end="")
            client(UpdateProfileRequest(
                first_name=random.choice(names), 
                last_name=random.choice(names)
                ))
            print("Done!")

# Set the schedule, ex: schedule.every(5).minutes.do(job)
        schedule.every().hour.do(job)

        job() # Launch immediately
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    main()

