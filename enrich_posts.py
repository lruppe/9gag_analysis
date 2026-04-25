import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    try:
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Attempt failed for URL: {url} with error: {e}")

def get_info_from_html(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('meta', property='og:title')['content']

    # Extract likes and comments
    description = soup.find('meta', property='og:description')['content']
    likes, comments = description.split(' • ')
    likes = int(likes.replace(' points', '').replace(',', ''))
    comments = int(comments.replace(' comments', '').replace(',', ''))
    # Extract image
    image = soup.find('meta', property='og:image')['content']
    return {
        'title': title,
        'likes': likes,
        'comments': comments,
        'image': image
    }

def get_image():
    # URL of the image
    url = "https://images-cdn.9gag.com/photo/aKqE0rW_ogimage_v2.jpg"
    headers = {
        "Host": "9gag.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=1",
        "TE": "trailers",
        "If-Modified-Since": "Sat, 25 May 2024 20:16:42 GMT"
    }

    cookies = {
        "sign_up_referer": "https://www.google.com/",
        "_ga": "GA1.2.645624004.1672943947",
        "auto_log": '{"a":false,"d":false,"lo":false,"dl":false}',
        "ts1": "0d4820ea09856d6024df707ca02aff72179d3f3a",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+May+25+2024+23%3A41%3A05+GMT%2B0200+(Mitteleurop%C3%A4ische+Sommerzeit)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=fd699e96-bb28-405f-8a30-306119d8802a&interactionCount=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0002%3A1%2CC0003%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=CH%3BZH",
        "OptanonAlertBoxClosed": "2024-05-25T21:41:05.654Z",
        "____ri": "9679",
        "____lo": "CH",
        "PHPSESSID": "ndc6haufde2opo50cokgl5ugo7",
        "session": "eyJpdiI6IlZSZ2ozUGRvRlwvTENcL2FySlFDZUt0Q01LNTFWdUxZZUZkREVsUm5UMnhtZz0iLCJ2YWx1ZSI6IjdmY05DaUZBN2tWRWlrTDBkRUFzbGZWbnlrQm1QWHVFVWdcLzdqMWR5ZkNPWGpPUHBcL1VtNllOQUhWaENKaEFBR1pmSlgyUW1QT2xYa3BDQUJTdWU5VFU0aHRaRkJtNStobGkxa0Q3RmRtTDhINXUwUWwzVlJBT2FZS1J4VE5ZdSszQk40cldpMWNJRlwvSXhSNUlheHhha292UlVvQzdYRFBpeUVJMDF0OElOZUx4WUhLcmtRXC9tOVhSdGVhckhxQWdDXC9BdCtySDFLWk5cL0RSemNQWXJ2dGlVbXFEMVZHK1VacHY2dXNjeDUzMWs5WXFGM2FPeUhpOTJ2a0t0b05FWUlsSHZnOEFkWk4xUFFVTU9SVEVvSjZmWnIyNDcyNktEK0FJQ1B6WnJiRTlhbHVzSjV2MFR4QnlGRVk5T0V3UmxTU0tMRFBGSTM0cEtTS3h1aDVuOUl6U2hTbXFuRXZ4amFZQUE4NXlYbzdNcUlHc1FJUHpudFBGN25nek5QNXlSalhoSHNQSlU0VHdvNEV2am5HcmNHWU5ocytNdE5cL3JxWXF1XC9wRVwvVDNLZCtHM2cxZjZrSmVLd0ZYSVI1ZFJwY29vVjlGM1RQdllja2NVVlR3cFFLaXZXbW1LK2VtdjFRVlRHbW5lWGRHcThpaU9zXC9sVDN5NnBBRm5SclBkcmx2MSIsIm1hYyI6IjM3MjIzNTNmMWY1ZDg5YTk1NmZmN2UxNDQ0ZDUyNTRkM2Q2NmEwZDVmNTZhYWVmNzIyNWNmZTI3MjVlNDBiYjcifQ==",
        "fbm_111569915535689": "base_domain=.9gag.com",
        "fbsr_111569915535689": "k8X9467ozFWfbWOC7EqETiuXSpdn4vUVakHO46hXDwQ.eyJ1c2VyX2lkIjoiNjQ4OTExMzk0IiwiY29kZSI6IkFRRFlwSHRaVlQ4NGdycmtHbFRrNlkwSlVhOGNOYTNXNV9sSDJrNjFuXzM1anFPVTNBMFVRclJDX1dzSGdPM0ZrQTd3RDZWTkFuODdYeU9MUVRuYVdaUE85Z2tRVGdPV09TbDI2TDRieUVXVG5VMGhMWk5xaThZbDNFenZ6RUtHaDVMNUh4N01jNHEzOFp3X3JyNm56N21KR29yYi1MbmR1cGFLLXdWLW5lb2dXNXVfM1lEdFdLNWNIbGxrRjJtT1FNeWEzcEl5R1UwLTRNLWdmeldVZ2VQbG1taXFUUEpfQTdWOElFWHlLWTV1QXZIOHc5d3IybU9QdjhpMV9RQkZuUmo4R2d6V2l4SWV5V3NoRXY5eWJNOHl1NXlrdDVEdjVxUXF5Y1FrTnV6bWJIczhGUjAwcFBISVBBNURUYjYyYlBFIiwib2F1dGhfdG9rZW4iOiJFQUFCbGVPVXU0VWtCT3hFWTltQ21TaFpBQjJIbnRBa3p6OUJGMklBSlRNbHA4andsZmJNV1VaQzgwaXFpUUh6N1BpUVhVZ01aQjVNRURISTFYTnZJYXNQR3V2M0hLQzZxTjhhaXlNeWJBM1lqaUsxbzFBV0JDZTV6S2Nob2xraDhpTkJyV0JrWW9rMlBPWVJnQ1c3YklzTXVqeG9WRWJEVHk4UVpBRjI1QXVIdHFGZXBvUU9KNzdCcWltamJRZUFuIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE3MTY2NzI5NTJ9"
    }
    # Send a GET request to the URL
    response = requests.get(url, headers, cookies=cookies)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary mode and write the content of the response
        with open("image.jpg", "wb") as file:
            file.write(response.content)
        print("Image saved successfully.")
    else:
        print("Failed to retrieve the image. Status code:", response.status_code)

if __name__ == '__main__':
    get_image()
    urls = ["http://9gag.com/gag/aNeQeb6","http://9gag.com/gag/aKqE0rW", "http://9gag.com/gag/aBYy1w2", "http://9gag.com/gag/ao9KrNg", "http://9gag.com/gag/aPDAoLq"]
    post_data = []
    for url in urls:
        html = get_html(url)
        info = get_info_from_html(html)
        post_data.append(info)
    for post in post_data:
        print(post)
