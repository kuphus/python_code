from web_handler import Web_handler


### Variables
username = 'uppie83@hotmail.com'
password = '79420666'
succes = False

while not succes:
    handler = Web_handler()
    handler.get('https://free-usenet.com/login/')

    handler.move_to_id('exampleInputEmail3')
    handler.type(username)
    handler.move_to_id('exampleInputPassword3')
    handler.type(password)
    handler.move_to_xpath('//button[@type="submit"]')
    handler.click()
    print('logged in')
    handler.move_to_xpath('//a[contains(text(),"Free account")]')
    handler.click()
    handler.switch_to_frame('//iframe[contains(@src, "google") and @role]', 5)
    handler.move_to_xpath_within_frame('//div[@class="recaptcha-checkbox-border"]')
    handler.switch_from_frame()
    handler.click_and_move_to_xpath('//button[@type="submit"]')

    if not handler.get_element_by_xpath('//iframe[@title="recaptcha challenge"]'):
        succes = True
        break
    else:
        handler.stop()

print('Tricked the recaptcha')
handler.click()