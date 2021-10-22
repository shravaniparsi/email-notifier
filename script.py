# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import json
import requests
from bs4 import BeautifulSoup
import smtplib
import configparser


def alert_via_email(url):

    header = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    email_msg = ""
    # url = "https://www.avaloncommunities.com/california/san-jose-apartments/avalon-on-the-alameda/apartments?bedroom=2BD"

    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    cards = soup.find_all(class_="apartment-card")
    email_content = []
    for card in cards:
        if card.find_all(class_="special-tag"):
            text = card.find(class_="content").find(class_="availability").get_text()
            price = card.find(class_="content").find(class_="price").get_text()
            price_in_int = price.replace(',','')[1:6]
            msg = ""
            if 'Dec' in text:
                msg="available special on month december \n availability:"+text+" \n price:"+price[0:6]
            email_content.append(msg)

    if(len(email_content) > 0):
        send_msg = '\n'.join(email_content)
        print(send_msg)
        send_email(send_msg)
    else:
        send_email("nothing new today!")

def send_email(send_msg):
    config = configparser.ConfigParser()
    config.read('email_info.ini')

    sender_email = 'shravaniparsi26@gmail.com'
    receiver_email = 'vishwakt@gmail.com'
    password_for_email = 'iamthegreatpinku'
    SUBJECT = "ALERT : Price Dropped for items your are tracking"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, send_msg)
    fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email,password_for_email)
    print("login is green")
    server.sendmail(sender_email,receiver_email,fmt.format(receiver_email, sender_email, SUBJECT, message).encode('utf-8'))
    print("email is sent")
    server.quit()


def main():
    alert_via_email("https://www.avaloncommunities.com/california/san-jose-apartments/avalon-morrison-park/apartments?bedroom=2BD")
    alert_via_email("https://www.avaloncommunities.com/california/san-jose-apartments/avalon-on-the-alameda/apartments?bedroom=2BD")


if __name__ == '__main__':
    main()


