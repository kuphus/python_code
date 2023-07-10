import time
import os
import concurrent.futures
import subprocess

## External libraries ##
import cv2
import soundfile as sf
import numpy as np


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class Video_player:


    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    #Methods
    def record_audio(self, length):
        audio = 'Stereo Mix (Conexant ISST Audio)'
        filename = 'test_audio.wav'
        print('starting ffmpeg')
        try:
            subprocess.run(['ffmpeg', '-f', 'dshow', '-i', f'audio={audio}', '-t', str(length), filename], capture_output=True, check=True)
            print('done with ffmpeg')
        except:
            print('recording failed')
            print('check if', audio, 'channel is available for recording')
        return filename


    def analyse_audio(self, file):
        print('analyzing ' + str(file))
        if os.path.isfile(file):
            rms = [np.sqrt(np.mean(block ** 2)) for block in
                sf.blocks(file, blocksize=1024, overlap=512)]
            average = sum(rms) / len(rms)
        else:
            print('File not found')
            average = 0
        return average


    def get_video_image(self, element):
        filename = 'screen_dump@' + str(time.time()) + '.png'
        element.screenshot(filename)
        print('screenshot taken')
        return filename


    def picture_difference(self, image1, image2):
        '''images need to be the same size/dimensions for comparison'''
        if os.path.isfile(image1) and os.path.isfile(image2):
            img1 = cv2.imread(image1)
            img2 = cv2.imread(image2)
            if img1.shape == img2.shape:
                difference = cv2.subtract(img1, img2)
                r, g, b = cv2.split(difference)
                non_zero = {
                    'r' : cv2.countNonZero(r),
                    'g' : cv2.countNonZero(g),
                    'b' : cv2.countNonZero(b),
                }
                return non_zero
            else:
                return -1
        else:
            print('Could not find (one of the) images')
            return 0-1


    def videoplayer_display_analysis(self, interval, length, element, delete=True):
        video_dumps = []
        start = time.time()
        end = start + length
        last_screenshot_time = start
        different_frames = 0
        while True:
            if time.time() >= end:
                filename = self.get_video_image(element)
                video_dumps.append(filename)
                break
            else:
                now = time.time()
                if now >= (last_screenshot_time + interval):
                    filename = self.get_video_image(element)
                    video_dumps.append(filename)
                    last_screenshot_time = now
        for index, file in enumerate(video_dumps):
            print('comparing images')
            if index > 0:
                difference = self.picture_difference(video_dumps[index], video_dumps[index-1])
                if difference['r'] > 0 or difference['g'] > 0 or difference['b'] > 0:
                    different_frames += 1
        if delete:
            self.remove_files(video_dumps)
        return different_frames


    def remove_files(self, list):
        for image in list:
            self.remove_file(image)
        list.clear()


    def remove_file(self,file):
        if os.path.isfile(file):
            print('removing file: ', file)
            os.remove(file)
        else:
            print('file', file, 'does not exist')


    def check_videoplayer(self, interval, length, xpath, min_diff_frames=1, delete=True):
        ''' This is the main method to call. Starts bij collecting the element associated with xpath.
            Starts recording the sound in a separate thread.
            Collects screenshots of the found element for every interval for length of time.
            Compares these schreenshot images to determine if one frame is different from the next.
            Analyzes the audio to determine average RMS.
            If the amount of different images if >= min_dif_frames video is detected.
            If the average RMS of the audio is above 0.001, audio is detected.
        '''
        element = self.get_element_by_xpath(xpath)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.record_audio, length)
            audio_filename = future.result()
        different_frames = self.videoplayer_display_analysis(interval, length, element, delete)
        average_rms = self.analyse_audio(audio_filename)
        if delete:
            self.remove_file(audio_filename)
        if different_frames >= min_diff_frames:
            video = True
            print('Video detected')
        else:
            video = False
            print('Video not detected')
        if average_rms > 0.001:
            audio = True
            print('Audio detected')
        else:
            audio = False
            print('Audio not detected')
        info = {
            'audio': audio,
            'video': video
        }
        return info

######################## TEST EXTRAS ##################################

    def get_element_by_xpath(self, xpath, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print('element found')
        except TimeoutException:
            element = None
        return element


    def go(self):
        dir_uname = 'appsquad'
        dir_pw = 'pctv-auth'
        self.driver.get('https://' + str(dir_uname) + ':' + str(dir_pw) + '@shaka.branch.tv.kpn.com/')
        login_button = self.get_element_by_xpath('//div[@class="RoundLongButton__Wrapper-f6dfk1-0 enVJFz RoundLong"]')
        login_button.click()
        login_met_abbo = self.get_element_by_xpath('//a[contains(text(),"Login met abonnementsnummer")]')
        login_met_abbo.click()
        username = self.get_element_by_xpath('//input[contains(@autocomplete, "username")]')
        username.clear()
        username.send_keys('20000004035432')
        pincode = self.get_element_by_xpath('//input[contains(@autocomplete, "password")]')
        pincode.clear()
        pincode.send_keys('6464')
        login_button2 = self.get_element_by_xpath('//span[contains(text(),"Inloggen")]')
        login_button2.click()

        first_pick = self.get_element_by_xpath('//div[@data-testid="carousel-slider__action-button"]', 15)
        self.driver.execute_script("arguments[0].click();", first_pick)
        nu_kijken = self.get_element_by_xpath('//button[@data-t="button-primary"]')
        nu_kijken.click()
        #sleep a little for the video to start playing
        time.sleep(3)


    def quit(self):
        self.driver.quit()


######################## END OF CLASS ########################



v1 = Video_player()
v1.go()

# player: //div[@data-t="player-container"]
# return button: //button[@class="button button--small button--overlay undefined"]
results = v1.check_videoplayer(2,10,'//div[@data-t="player-container"]')
print('results: ', results)
v1.quit()
