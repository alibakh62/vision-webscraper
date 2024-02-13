import openai
import subprocess
import base64
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def image_base64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()


def url2screenshot(url):
    print(f"Crawling {url}")

    if os.path.exists("screenshot.jpg"):
        os.remove("screenshot.jpg")

    result = subprocess.run(
        ["node", "takeScreenshot.js", url],
        capture_output=True,
        text=True,
    )

    exitcode = result.returncode
    output = result.stdout

    if exitcode != 0:
        print(f"Error: {output}")
        return None

    if not os.path.exists("screenshot.jpg"):
        print("Error: Screenshot not found")
        return None

    b64_image = image_base64("screenshot.jpg")

    return b64_image


def gptv_extract(b64_image, prompt):
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction",
            }
        ]
        + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        max_tokens=1024,
    )

    message = response.choices[0].message
    message_text = message.content

    if "ANSWER_NOT_FOUND" in message_text:
        print("Error: Answer not found")
        return "Could not find the answer"
    else:
        print(f"Answer: {message_text}")
        return message_text


def gptv_crawl(url, prompt):
    b64_image = url2screenshot(url)
    if b64_image == "Error: Screenshot not found":
        return "Error: Couldn't crawl the website"
    else:
        return gptv_extract(b64_image, prompt)
