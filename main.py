from pathlib import Path
from app.processor import process

import cv2
if __name__ == "__main__":
    path = Path.joinpath(Path.cwd(),"json","HSVdata.json")
    process = process(path=path,using_camera=False)

    while(True):
        return_map = process.run()

        #show images
        images = return_map["images"]
        for image in images:
            cv2.imshow(image["title"],image["image"])

        #show debug messages
        messages = return_map["messages"]
        for msg in messages:
            print(msg)

        k = cv2.waitKey(1)
        if k == 27: # if the user wants to exit the program 
            break
        if k == 83:
            process.image_fetcher.next()
        if k == 81:
            process.image_fetcher.prev()
    process.end()

