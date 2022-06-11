import json
import re
import uuid
from io import BytesIO

import execjs
import requests
from PIL import Image

from GeeTest.Customer import get_customer_slide_data, get_slide_data_v2
from GeeTest.OCR import get_distance, get_distance2
from GeeTest.Slider import get_slide_track


class GeeTestMain:
    def __init__(self):
        # 主要路径
        self.main_url = "https://www.geetest.com/"
        # 静态文件路径
        self.static_url = "https://static.geetest.com/"
        # 加载请求路径
        self.load_url = "https://gcaptcha4.geetest.com/load"
        # 校验路径
        self.verify_url = "https://gcaptcha4.geetest.com/verify"
        # 请求
        self.request = requests.session()
        self.request.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30 "
        }
        # js
        self.exec = execjs.compile(open('js/GeeTest.js', mode='r', encoding='utf-8').read())
        # 变量
        self.captcha_id = self.get_captcha_id_init()
        self.challenge = None
        self.lot_number = None
        # 背景图片
        self.bg_img_url = None
        # 滑块图片
        self.slice_img_url = None
        # 滑块缺口距离
        self.distance = None
        # 鼠标轨迹
        self.slide_data = None
        # 参数
        self.datetime = None
        self.payload = None
        self.process_token = None
        self.payload_protocol = None
        self.count = 0

    def get_captcha_id_init(self):
        url = f'{self.main_url}adaptive-captcha-demo'
        res = self.request.get(url).text
        # 获取js请求地址
        js_link = re.search(r'_next/static/(.*)/pages/adaptive-captcha-demo.js', res).group()
        # 获取js文件
        res = self.request.get(f'{self.main_url}{js_link}').text
        captcha_id = re.search(r'captchaId:"(.*)",product', res).group(1)
        return captcha_id

    def get_challenge(self):
        challenge = uuid.uuid4()
        self.challenge = challenge
        return challenge

    def load(self):
        url = f'{self.load_url}?' \
              f'captcha_id={self.captcha_id}&' \
              f'challenge={self.get_challenge()}&client_type=web&risk_type=slide&lang=zh&callback=geetest_1654222782756'
        res = self.request.get(url).text
        data = res.replace('geetest_1654222782756(', '').replace(")", "")
        data = json.loads(data)
        self.lot_number = data['data']['lot_number']
        self.bg_img_url = self.static_url + data['data']['bg']
        self.slice_img_url = self.static_url + data['data']['slice']
        self.datetime = data['data']['pow_detail']['datetime']
        self.payload = data['data']["payload"]
        self.process_token = data['data']["process_token"]
        self.payload_protocol = data['data']["payload_protocol"]
        return self

    def image_recognition(self, bg_image_path='image/bg.png', slice_image_path='image/slice.png'):
        """
        图片识别
        :return:
        """
        bg_image_content = self.request.get(self.bg_img_url).content
        slice_image_content = self.request.get(self.slice_img_url).content
        image = Image.open(BytesIO(bg_image_content))
        image.save(bg_image_path)
        image = Image.open(BytesIO(slice_image_content))
        image.save(slice_image_path)
        distance = get_distance2(bg=bg_image_path,
                                tp=slice_image_path
                                )
        # 滑块距离
        self.distance = distance
        # 生成鼠标轨迹
        # self.slide_data = get_slide_track(distance)
        # self.slide_data = get_customer_slide_data(distance)
        self.slide_data = get_slide_data_v2(distance)
        print('滑块轨迹：', self.slide_data)
        return self

    def get_w(self, captcha_width=300):
        """
        获取W值
        :param captcha_width: 图片长度
        :return:
        """
        return self.exec.call('get_w', self.slide_data, captcha_width, self.lot_number)

    def verify(self):
        w = self.get_w()
        print('w:', w)
        url = f'{self.verify_url}?captcha_id={self.captcha_id}&client_type=web&lot_number={self.lot_number}&' \
              f'risk_type=slide&pt=1&lang=zho&payload={self.payload}&' \
              f'process_token={self.process_token}&pt=1' \
              f'&w={w}&callback=geetest_1654239866960'
        res = self.request.get(url).text
        res = res.replace('geetest_1654239866960(', '').replace(")", "")
        data = json.loads(res)
        # print(data)
        if res.find('result') > -1 and data['data']['result'] == 'success':
            print(' \033[1;35m 识别通过 \033[0m ->', res)
            self.count += 1
        return self

    def passing_rate(self, cyc):
        if self.count == 0:
            print(f"通过率：0%，成功：0，失败：{cyc}")
        else:
            print(f'通过率：{(self.count / cyc) * 100}%，成功：{self.count}，失败：{cyc - self.count}')


if __name__ == '__main__':
    cycles = 100
    gee = GeeTestMain()
    for i in range(cycles):
        gee.load().image_recognition().verify()
    gee.passing_rate(cycles)
