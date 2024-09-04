from playwright.sync_api import sync_playwright
import json
import time
import inference
import requests
from PIL import Image
import sys
import warnings
from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore")

def get_embedding(sentence):
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModel.from_pretrained('distilbert-base-uncased')
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach()

def get_object(question):
    objects = ["boat","book","camera","chair","american football","guitar","hat","tree", "basketball", "purse", "pineapple", "car"]
    object_embeddings = []

    for obj in objects:
        object_embeddings.append(get_embedding(obj))
    
    question_embedding = get_embedding(question)

    similarities = []

    for obj in object_embeddings:
        similarities.append(cosine_similarity(question_embedding, obj).item())

    best_match_idx = torch.argmax(torch.tensor(similarities))
    best_match = objects[best_match_idx]

    return best_match



def get_image_src(page):
    image_url = page.get_attribute("img#captcha-verify-image", "src")
    return image_url

def download_image(image_url):
    response = requests.get(image_url)
    image_path = "captcha_image.jpg"
    with open(image_path, "wb") as f:
        f.write(response.content)
    return image_path


def run_inference_on_image_tougher(image_path, object):

    found_proper = False

    model = inference.get_model("captcha-2-6ehbe/1")
    results = model.infer(image=image_path)

    class_names = []
    bounding_boxes = []
    for obj in results[0].predictions:
        class_names.append(obj.class_name)
        bounding_boxes.append({
            "x": obj.x,
            "y": obj.y,
            "width": obj.width,
            "height": obj.height
        })
    
    bounding_box = []
    class_to_click = object
    for i, classes in enumerate(class_names):
        if classes == class_to_click:
            bounding_box.append(bounding_boxes[i])
    
    if len(bounding_box) == 2:
        found_proper = True

    return bounding_box, found_proper

def run_inference_on_image(image_path):

    model = inference.get_model("tk-3nwi9/2")
    results = model.infer(image=image_path)

    class_names = []
    bounding_boxes = []
    for obj in results[0].predictions:
        class_names.append(obj.class_name)
        bounding_boxes.append({
            "x": obj.x,
            "y": obj.y,
            "width": obj.width,
            "height": obj.height
        })
    
    already_written = []
    bounding_box = []
    class_to_click = []
    for i, classes in enumerate(class_names):
        if classes in already_written:
            class_to_click.append(classes)
            bounding_box.append(bounding_boxes[i])
            index = already_written.index(classes)
            bounding_box.append(bounding_boxes[index])
        
        already_written.append(classes)


    return bounding_box, class_to_click

def convert_to_webpage_coordinates(bounding_boxes, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real):

    webpage_coordinates = []
    for box in bounding_boxes:
        x_box = box['x']
        y_box = box['y']
        rel_x = (x_box * image_width_web) / image_width_real
        rel_y = (y_box * image_height_web) / image_height_real
        x_cord = image_x + rel_x 
        y_cord = image_y + rel_y

        print(f'BOX_X: {rel_x} : BOX_Y: {rel_y}')
        
        webpage_coordinates.append((x_cord, y_cord))
    
    return webpage_coordinates

def click_on_objects(page, object_coords):
    for (x, y) in object_coords:
        page.mouse.click(x, y)
        time.sleep(0.5)



def upload_tiktok(video, description, hashtags, cookies_path, sound_name=None, sound_aud_vol='mix', schedule=None, day=None, copyrightcheck=False):

    """
    UPLOADS VIDEO TO TIKTOK
    ------------------------------------------------------------------------------------------------------------------------------------------------c
    video (str) -> path to video to upload
    description (str) -> description for video
    hashtags (str)(array) -> hashtags for video
    cookies_path (str) -> path to tik tok cookies .json file
    sound_name (str) -> name of tik tok sound to use for video
    sound_aud_vol (str) -> volume of tik tok sound, 'main', 'mix' or 'background', check documentation for more info -> https://github.com/haziq-exe/TikTokAutoUploader
    schedule (str) -> format HH:MM, your local time to upload video
    day (int) -> day to schedule video for, check documentation for more info -> https://github.com/haziq-exe/TikTokAutoUploader
    copyrightcheck (bool) -> include copyright check or not; CODE FAILS IF DONT PASS COPYRIGHT CHECK
    --------------------------------------------------------------------------------------------------------------------------------------------
    """

    retries = 0
    class_found = None

    try:
        with open(cookies_path , 'r') as cookiefile:
            cookies = json.load(cookiefile)
    except:
        sys.exit("ERROR: COOKIES FILE NOT FOUND, make sure to copy the path of the cookies.json file")

    try:
        for cookie in cookies:
            if cookie.get('sameSite') not in ['Strict', 'Lax', 'None']:
                cookie['sameSite'] = 'Lax'
    except:
        sys.exit("ERROR: CANT READ COOKIES FILE, make sure the data in cookies.json is correct and in a valid format")
    

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        url = 'https://www.tiktok.com/tiktokstudio/upload?from=upload&lang=en'

        while retries < 2:
            try:
                page.goto(url, timeout=60000)
            except:
                retries +=1
                time.sleep(5)
                if retries == 2:
                    sys.exit("ERROR: TIK TOK PAGE FAILED TO LOAD, try again.")
            else:
                break

        
        image = get_image_src(page)
        if image:
            solved = False
            attempts = 0
            while solved == False:
                attempts += 1
                question = page.locator('div.VerifyBar___StyledDiv-sc-12zaxoy-0.hRJhHT').text_content()
                if 'Select two objects that are the same' in question:
                    while class_found == None:
                        page.click('span.secsdk_captcha_refresh--text')
                        time.sleep(0.5)
                        image = get_image_src(page)
                        img_path = download_image(image)
                        b_box, class_found = run_inference_on_image(image_path=img_path)
                        print(f'CLICKING ON {class_found}')
                    
                    with Image.open(img_path) as img:
                        image_size = img.size
                
                    image = page.locator('#captcha-verify-image')
                    image.wait_for()
                    box = image.bounding_box()
                    image_x = box['x']
                    image_y = box['y']
                    image_height_web = box['height']
                    image_width_web = box['width']
                    image_width_real, image_height_real = image_size

                    webpage_coords = convert_to_webpage_coordinates(b_box, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real)
                    click_on_objects(page, webpage_coords)
                    time.sleep(0.5)
                    page.click("div.verify-captcha-submit-button")
                    if attempts > 5:
                        sys.exit("FAILED TO SOLVE CAPTCHA")
                    try:
                        page.wait_for_selector('input[type="file"][accept="video/*"]', timeout=5000)
                        solved = True
                    except:
                        continue
                else:
                    found_prop = False
                    while found_prop == False:
                        page.click('span.secsdk_captcha_refresh--text')
                        time.sleep(0.5)
                        object = get_object(question)
                        image = get_image_src(page)
                        img_path = download_image(image)
                        if object == 'american football':
                            object = 'football'
                        b_box, found_prop = run_inference_on_image_tougher(image_path=img_path, object=object)
                    
                    with Image.open(img_path) as img:
                        image_size = img.size
                
                    image = page.locator('#captcha-verify-image')
                    image.wait_for()
                    box = image.bounding_box()
                    image_x = box['x']
                    image_y = box['y']
                    image_height_web = box['height']
                    image_width_web = box['width']
                    image_width_real, image_height_real = image_size

                    webpage_coords = convert_to_webpage_coordinates(b_box, image_x, image_y, image_height_web, image_width_web, image_height_real, image_width_real)
                    click_on_objects(page, webpage_coords)
                    time.sleep(0.5)
                    page.click("div.verify-captcha-submit-button")
                    if attempts > 5:
                        sys.exit("FAILED TO SOLVE CAPTCHA")
                    try:
                        page.wait_for_selector('input[type="file"][accept="video/*"]', timeout=5000)
                        solved = True
                    except:
                        continue


        
        try:
            page.wait_for_selector('input[type="file"][accept="video/*"]', timeout=30000)
            page.set_input_files('input[type="file"][accept="video/*"]', f'{video}')
        except:
            sys.exit("ERROR: INPUT FILE FAILED TO UPLOAD. Possible Issues: Wifi too slow, file directory wrong, or check documentation to see if captcha is solvable")

        page.wait_for_selector('div[data-contents="true"]')
        page.click('div[data-contents="true"]')
        time.sleep(0.5)
        if description == None:
            sys.exit("ERROR: PLEASE INCLUDE A DESCRIPTION")

        for _ in range(len(video) + 2):
            page.keyboard.press("Backspace")
            page.keyboard.press("Delete")
        
        time.sleep(0.5)

        page.keyboard.type(description)

        for _ in range(3):
            page.keyboard.press("Enter")

        if hashtags != None:
            for hashtag in hashtags:
                if hashtag[0] != '#':
                    hashtag = "#" + hashtag

                page.keyboard.type(hashtag)
                time.sleep(0.5)
                try:
                    page.click(f'span.hash-tag-topic:has-text("{hashtag}")', timeout=1000)
                except:
                    try:
                        page.click('span.hash-tag-topic', timeout=1000)
                    except:
                        page.keyboard.press("Backspace")
                        try:
                            page.click('span.hash-tag-topic', timeout=1000)
                        except:
                            print(f"Tik tok hashtag not working for {hashtag}, moving onto next")
                            for _ in range(len(hashtag) + 1):
                                page.keyboard.press("Backspace")

        try:
            page.wait_for_function("document.querySelector('.info-progress-num').textContent.trim() === '100%'", timeout=3000000)  
        except:
            sys.exit("ERROR: TIK TOK TOOK TOO LONG TO UPLOAD YOUR FILE (>50min). try a lower file size or different wifi connection")

        time.sleep(0.5)

        page.click('button.TUXButton.TUXButton--default.TUXButton--large.TUXButton--secondary:has-text("Save draft")')
        page.wait_for_selector("path[d='M37.37 4.85a4.01 4.01 0 0 0-.99-.79 3 3 0 0 0-2.72 0c-.45.23-.81.6-1 .79a9 9 0 0 1-.04.05l-19.3 19.3c-1.64 1.63-2.53 2.52-3.35 3.47a36 36 0 0 0-4.32 6.16c-.6 1.1-1.14 2.24-2.11 4.33l-.3.6c-.4.75-.84 1.61-.8 2.43a2.5 2.5 0 0 0 2.37 2.36c.82.05 1.68-.4 2.44-.79l.59-.3c2.09-.97 3.23-1.5 4.33-2.11a36 36 0 0 0 6.16-4.32c.95-.82 1.84-1.71 3.47-3.34l19.3-19.3.05-.06a3 3 0 0 0 .78-3.71c-.22-.45-.6-.81-.78-1l-.02-.02-.03-.03-3.67-3.67a8.7 8.7 0 0 1-.06-.05ZM16.2 26.97 35.02 8.15l2.83 2.83L19.03 29.8c-1.7 1.7-2.5 2.5-3.33 3.21a32 32 0 0 1-7.65 4.93 32 32 0 0 1 4.93-7.65c.73-.82 1.51-1.61 3.22-3.32Z']")
        page.click("path[d='M37.37 4.85a4.01 4.01 0 0 0-.99-.79 3 3 0 0 0-2.72 0c-.45.23-.81.6-1 .79a9 9 0 0 1-.04.05l-19.3 19.3c-1.64 1.63-2.53 2.52-3.35 3.47a36 36 0 0 0-4.32 6.16c-.6 1.1-1.14 2.24-2.11 4.33l-.3.6c-.4.75-.84 1.61-.8 2.43a2.5 2.5 0 0 0 2.37 2.36c.82.05 1.68-.4 2.44-.79l.59-.3c2.09-.97 3.23-1.5 4.33-2.11a36 36 0 0 0 6.16-4.32c.95-.82 1.84-1.71 3.47-3.34l19.3-19.3.05-.06a3 3 0 0 0 .78-3.71c-.22-.45-.6-.81-.78-1l-.02-.02-.03-.03-3.67-3.67a8.7 8.7 0 0 1-.06-.05ZM16.2 26.97 35.02 8.15l2.83 2.83L19.03 29.8c-1.7 1.7-2.5 2.5-3.33 3.21a32 32 0 0 1-7.65 4.93 32 32 0 0 1 4.93-7.65c.73-.82 1.51-1.61 3.22-3.32Z']")
        page.wait_for_selector('div[data-contents="true"]')
        page.wait_for_function("document.querySelector('.info-progress-num').textContent.trim() === '100%'", timeout=3000000)  
        time.sleep(0.5)

        if sound_name != None:
            page.click("div.TUXButton-label:has-text('Edit video')")
            page.wait_for_selector("input.search-bar-input")
            page.fill(f"input.search-bar-input", f"{sound_name}")
            time.sleep(0.5)
            page.click("div.TUXButton-label:has-text('Search')")
            page.wait_for_selector('div.music-card-container')
            page.click("div.music-card-container")
            time.sleep(0.5)
            page.click("div.TUXButton-label:has-text('Use')")
            time.sleep(0.5)
            page.click('img[src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjEiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMSAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTAgNy41MDE2QzAgNi42NzMxNyAwLjY3MTU3MyA2LjAwMTYgMS41IDYuMDAxNkgzLjU3NzA5QzMuODY4MDUgNi4wMDE2IDQuMTQ0NTggNS44NzQ4OCA0LjMzNDU1IDUuNjU0NDlMOC43NDI1NSAwLjU0MDUyQzkuMzQ3OCAtMC4xNjE2NjggMTAuNSAwLjI2NjM3NCAxMC41IDEuMTkzNDFWMTguOTY3MkMxMC41IDE5Ljg3NDUgOS4zODg5NCAyMC4zMTI5IDguNzY5NDIgMTkuNjVMNC4zMzE3OSAxNC45MDIxQzQuMTQyNjkgMTQuNjk5OCAzLjg3ODE2IDE0LjU4NDkgMy42MDEyMiAxNC41ODQ5SDEuNUMwLjY3MTU3MyAxNC41ODQ5IDAgMTMuOTEzNCAwIDEzLjA4NDlWNy41MDE2Wk01Ljg0OTQ1IDYuOTYwMjdDNS4yNzk1NiA3LjYyMTQzIDQuNDQ5OTcgOC4wMDE2IDMuNTc3MDkgOC4wMDE2SDJWMTIuNTg0OUgzLjYwMTIyQzQuNDMyMDMgMTIuNTg0OSA1LjIyNTY0IDEyLjkyOTUgNS43OTI5NSAxMy41MzY0TDguNSAxNi40MzI4VjMuODg1MjJMNS44NDk0NSA2Ljk2MDI3WiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPHBhdGggZD0iTTEzLjUxNSA3LjE5MTE5QzEzLjM0MjQgNi45NzU1OSAxMy4zMzk5IDYuNjYwNTYgMTMuNTM1MiA2LjQ2NTNMMTQuMjQyMyA1Ljc1ODE5QzE0LjQzNzYgNS41NjI5MyAxNC43NTU4IDUuNTYxNzUgMTQuOTM1NiA1Ljc3MTM2QzE2Ljk5NTkgOC4xNzM2MiAxNi45OTU5IDExLjgyOCAxNC45MzU2IDE0LjIzMDNDMTQuNzU1OCAxNC40Mzk5IDE0LjQzNzYgMTQuNDM4NyAxNC4yNDIzIDE0LjI0MzVMMTMuNTM1MiAxMy41MzY0QzEzLjMzOTkgMTMuMzQxMSAxMy4zNDI0IDEzLjAyNjEgMTMuNTE1IDEyLjgxMDVDMTQuODEzIDExLjE4ODUgMTQuODEzIDguODEzMTIgMTMuNTE1IDcuMTkxMTlaIiBmaWxsPSIjMTYxODIzIiBmaWxsLW9wYWNpdHk9IjAuNiIvPgo8cGF0aCBkPSJNMTYuNzE3MiAxNi43MTgzQzE2LjUyMTkgMTYuNTIzMSAxNi41MjMxIDE2LjIwNzQgMTYuNzA3MiAxNi4wMDE3QzE5LjcyNTcgMTIuNjMgMTkuNzI1NyA3LjM3MTY4IDE2LjcwNzIgNC4wMDAwMUMxNi41MjMxIDMuNzk0MjcgMTYuNTIxOSAzLjQ3ODU4IDE2LjcxNzIgMy4yODMzMkwxNy40MjQzIDIuNTc2MjFDMTcuNjE5NSAyLjM4MDk1IDE3LjkzNyAyLjM4MDIgMTguMTIzMyAyLjU4NDA4QzIxLjkwOTkgNi43MjkyNiAyMS45MDk5IDEzLjI3MjQgMTguMTIzMyAxNy40MTc2QzE3LjkzNyAxNy42MjE1IDE3LjYxOTUgMTcuNjIwNyAxNy40MjQzIDE3LjQyNTVMMTYuNzE3MiAxNi43MTgzWiIgZmlsbD0iIzE2MTgyMyIgZmlsbC1vcGFjaXR5PSIwLjYiLz4KPC9zdmc+Cg=="]')
            time.sleep(0.5)
            sliders = page.locator("input.scaleInput")
            time.sleep(0.5)

            if sound_aud_vol == 'background':
                slider1 = sliders.nth(0)
                bounding_box1 = slider1.bounding_box()
                if bounding_box1:
                    x1 = bounding_box1["x"] + (bounding_box1["width"] * 0.95)
                    y1 = bounding_box1["y"] + bounding_box1["height"] / 2
                    page.mouse.click(x1, y1)
            
                slider2 = sliders.nth(1)
                bounding_box2 = slider2.bounding_box()
                if bounding_box2:
                    x2 = bounding_box2["x"] + (bounding_box2["width"] * 0.097)
                    y2 = bounding_box2["y"] + bounding_box2["height"] / 2
                    page.mouse.click(x2, y2)

            if sound_aud_vol == 'main':
                slider1 = sliders.nth(0)
                bounding_box1 = slider1.bounding_box()
                if bounding_box1:
                    x1 = bounding_box1["x"] + (bounding_box1["width"] * 0.097)
                    y1 = bounding_box1["y"] + bounding_box1["height"] / 2
                    page.mouse.click(x1, y1)
                slider2 = sliders.nth(1)
                bounding_box2 = slider2.bounding_box()
                if bounding_box2:
                    x2 = bounding_box2["x"] + (bounding_box2["width"] * 0.95)
                    y2 = bounding_box2["y"] + bounding_box2["height"] / 2
                    page.mouse.click(x2, y2)   


            time.sleep(0.5)
            page.click("div.TUXButton-label:has-text('Save edit')")
            
        page.wait_for_selector('div[data-contents="true"]')
        if schedule != None:
            try:
                hour = schedule[0:2]
                minute = schedule[3:]
                print(hour, minute)
                if (int(minute) % 5) != 0:
                    sys.exit("MINUTE FORMAT ERROR: PLEASE MAKE SURE MINUTE YOU SCHEDULE AT IS A MULTIPLE OF 5 UNTIL 60 (i.e: 40)")

            except:
                sys.exit("SCHEDULE TIME ERROR: PLEASE MAKE SURE YOUR SCHEDULE TIME IS A STRING THAT FOLLOWS THE 24H FORMAT 'HH:MM'")

            page.locator('div.TUXRadioStandalone.TUXRadioStandalone--medium').nth(1).click()
            time.sleep(0.5)
            if day != None:
                page.locator('div.TUXTextInputCore-trailingIconWrapper').nth(1).click()
                time.sleep(0.5)
                try:
                    page.locator(f'span.day.valid:has-text("{day}")').click()
                except:
                    sys.exit("SCHEDULE DAY ERROR: ERROR WITH SCHEDULED DAY, read documentation for more information on format of day")
            try:
                page.locator('div.TUXTextInputCore-trailingIconWrapper').nth(0).click()
                time.sleep(0.5)
                page.locator(f'.tiktok-timepicker-option-text:has-text("{hour}")').nth(0).scroll_into_view_if_needed()
                page.locator(f'.tiktok-timepicker-option-text:has-text("{hour}")').nth(0).click()
                time.sleep(1)
                page.locator('div.TUXTextInputCore-trailingIconWrapper').nth(0).click()
                time.sleep(0.5)
                page.locator(f'.tiktok-timepicker-option-text:has-text("{minute}")').nth(1).scroll_into_view_if_needed()
                time.sleep(0.5)
                page.locator(f'.tiktok-timepicker-option-text:has-text("{minute}")').nth(1).click()

                error_message_locator = page.locator('span', has_text="Schedule at least 15 minutes in advance")
                if error_message_locator.is_visible():
                    sys.exit("SCHEDULE TIME ERROR: SCHEDULING TIME SHOULD BE MORE THAN 15 MINUTES FROM YOUR CURRENT TIME")

            except:
                sys.exit("SCHEDULING ERROR")
            



        if copyrightcheck == True:
            page.locator("input#\\:r1h\\: + div.TUXSwitch-handle").click()
            while copyrightcheck == True:
                time.sleep(3)
                if page.locator("span", has_text="No issues detected.").is_visible():
                    break
                if page.locator("span", has_text="Copyright issues detected.").is_visible():
                    sys.exit("COPYRIGHT CHECK FAILED: COPYRIGHT AUDIO DETECTED FROM TIKTOK")
        

        page.click('button.TUXButton.TUXButton--default.TUXButton--large.TUXButton--primary')
        time.sleep(2)

        page.close()