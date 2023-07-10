import Browser, time

browser = Browser.Browser()
browser.new_browser(headless=False)
browser.new_page("https://grabpoints.com/#/login")

continue_button = "//button[contains(@class, 'login-button')]"
email_input = "//input[@name='email']" 
password_input = "//input[@name='password']" 
email = "kevin.uphus.werk@gmail.com"
ww = "B0w1EM@rL3y"

browser.type_text(email_input, email)
browser.type_secret(password_input, ww)
browser.click(continue_button)
time.sleep(20)
browser.take_screenshot(filename='test_pic')


#links_on_page = browser.get_elements("//ol//li//a")
#print(len(links_on_page))
#assert 'Playwright' in browser.get_text("h1")
browser.close_browser()