#!/usr/bin/env python
# -*- coding: utf-8 -*-

# refer to `https://bitbucket.org/akorn/wheezy.captcha`

import random
import string
import os.path
from io import BytesIO

from PIL import Image
from PIL import ImageFilter
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype


class Bezier:
    def __init__(self):
        self.tsequence = tuple([t / 20.0 for t in range(21)])
        self.beziers = {}

    def pascal_row(self, n):
        """ Returns n-th row of Pascal's triangle
        """
        result = [1]
        x, numerator = 1, n
        for denominator in range(1, n // 2 + 1):
            x *= numerator
            x /= denominator
            result.append(x)
            numerator -= 1
        if n & 1 == 0:
            result.extend(reversed(result[:-1]))
        else:
            result.extend(reversed(result))
        return result

    def make_bezier(self, n):
        """ Bezier curves:
            http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        """
        try:
            return self.beziers[n]
        except KeyError:
            combinations = self.pascal_row(n - 1)
            result = []
            for t in self.tsequence:
                tpowers = (t ** i for i in range(n))
                upowers = ((1 - t) ** i for i in range(n - 1, -1, -1))
                coefs = [c * a * b for c, a, b in zip(combinations,
                                                      tpowers, upowers)]
                result.append(coefs)
            self.beziers[n] = result
            return result


class Captcha(object):
    def __init__(self):
        self._bezier = Bezier()
        self._dir = os.path.dirname(__file__)
        # self._captcha_path = os.path.join(self._dir, '..', 'static', 'captcha')

    @staticmethod
    def instance():
        if not hasattr(Captcha, "_instance"):
            Captcha._instance = Captcha()
        return Captcha._instance

    def initialize(self, width=200, height=75, color=None, text=None, fonts=None):
        # self.image = Image.new('RGB', (width, height), (255, 255, 255))
        self._text = text if text else random.sample(string.ascii_uppercase + string.ascii_uppercase + '3456789', 4)
        self.fonts = fonts if fonts else \
            [os.path.join(self._dir, 'fonts', font) for font in ['Arial.ttf', 'Georgia.ttf', 'actionj.ttf']]
        self.width = width
        self.height = height
        self._color = color if color else self.random_color(0, 200, random.randint(220, 255))

    @staticmethod
    def random_color(start, end, opacity=None):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        if opacity is None:
            return red, green, blue
        return red, green, blue, opacity

    # draw image

    def background(self, image):
        Draw(image).rectangle([(0, 0), image.size], fill=self.random_color(238, 255))
        return image

    @staticmethod
    def smooth(image):
        return image.filter(ImageFilter.SMOOTH)

    def curve(self, image, width=4, number=6, color=None):
        dx, height = image.size
        dx /= number
        path = [(dx * i, random.randint(0, height))
                for i in range(1, number)]
        bcoefs = self._bezier.make_bezier(number - 1)
        points = []
        for coefs in bcoefs:
            points.append(tuple(sum([coef * p for coef, p in zip(coefs, ps)])
                                for ps in zip(*path)))
        Draw(image).line(points, fill=color if color else self._color, width=width)
        return image

    def noise(self, image, number=50, level=2, color=None):
        width, height = image.size
        dx = width / 10
        width -= dx
        dy = height / 10
        height -= dy
        draw = Draw(image)
        for i in range(number):
            x = int(random.uniform(dx, width))
            y = int(random.uniform(dy, height))
            draw.line(((x, y), (x + level, y)), fill=color if color else self._color, width=level)
        return image

    def text(self, image, fonts, font_sizes=None, drawings=None, squeeze_factor=0.75, color=None):
        color = color if color else self._color
        fonts = tuple([truetype(name, size)
                       for name in fonts
                       for size in font_sizes or (65, 70, 75)])
        draw = Draw(image)
        char_images = []
        for c in self._text:
            font = random.choice(fonts)
            c_width, c_height = draw.textsize(c, font=font)
            char_image = Image.new('RGB', (c_width, c_height), (0, 0, 0))
            char_draw = Draw(char_image)
            char_draw.text((0, 0), c, font=font, fill=color)
            char_image = char_image.crop(char_image.getbbox())
            for drawing in drawings:
                d = getattr(self, drawing)
                char_image = d(char_image)
            char_images.append(char_image)
        width, height = image.size
        offset = int((width - sum(int(i.size[0] * squeeze_factor)
                                  for i in char_images[:-1]) -
                      char_images[-1].size[0]) / 2)
        for char_image in char_images:
            c_width, c_height = char_image.size
            mask = char_image.convert('L').point(lambda i: i * 1.97)
            image.paste(char_image,
                        (offset, int((height - c_height) / 2)),
                        mask)
            offset += int(c_width * squeeze_factor)
        return image

    # draw text
    @staticmethod
    def warp(image, dx_factor=0.27, dy_factor=0.21):
        width, height = image.size
        dx = width * dx_factor
        dy = height * dy_factor
        x1 = int(random.uniform(-dx, dx))
        y1 = int(random.uniform(-dy, dy))
        x2 = int(random.uniform(-dx, dx))
        y2 = int(random.uniform(-dy, dy))
        image2 = Image.new('RGB',
                           (width + abs(x1) + abs(x2),
                            height + abs(y1) + abs(y2)))
        image2.paste(image, (abs(x1), abs(y1)))
        width2, height2 = image2.size
        return image2.transform(
            (width, height), Image.QUAD,
            (x1, y1,
             -x1, height2 - y2,
             width2 + x2, height2 + y2,
             width2 - x2, -y1))

    @staticmethod
    def offset(image, dx_factor=0.1, dy_factor=0.2):
        width, height = image.size
        dx = int(random.random() * width * dx_factor)
        dy = int(random.random() * height * dy_factor)
        image2 = Image.new('RGB', (width + dx, height + dy))
        image2.paste(image, (dx, dy))
        return image2

    @staticmethod
    def rotate(image, angle=25):
        return image.rotate(
            random.uniform(-angle, angle), Image.BILINEAR, expand=1)

    def captcha(self, path=None, fmt='JPEG'):
        """Create a captcha.

        Args:
            path: save path, default None.
            fmt: image format, PNG / JPEG.
        Returns:
            A tuple, (name, text, StringIO.value).
            For example:
                ('fXZJN4AFxHGoU5mIlcsdOypa', 'JGW9', '\x89PNG\r\n\x1a\n\x00\x00\x00\r...')

        """
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        image = self.background(image)
        image = self.text(image, self.fonts, drawings=['warp', 'rotate', 'offset'])
        image = self.curve(image)
        image = self.noise(image)
        image = self.smooth(image)
        name = "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + '3456789', 24))
        text = "".join(self._text)
        out = BytesIO()
        image.save(out, format=fmt)
        if path:
            image.save(os.path.join(path, name), fmt)
        return name, text, out.getvalue()

    def generate_captcha(self):
        self.initialize()
        return self.captcha()


captcha = Captcha.instance()


"""
import random
import string
# Image:一个画布
# ImageDraw:一个画笔
# ImageFont:画笔的字体

# pip install pillow
from PIL import Image, ImageDraw, ImageFont


class Captcha(object):
    # 生成几位数的验证码
    number = 4
    # 验证码图片的高度和宽度
    size = (100, 30)
    # 验证码字体大小
    fontsize = 25
    # 加入干扰线条数
    line_number = 2

    # 构建一个验证码源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 用来绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成随机的颜色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    # 随机选择一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'arial.ttf',
            'calibrib.ttf'
        ]
        font = random.choice(fonts)
        return 'utils/captcha/' + font

    # 用来随机生成一个字符串
    @classmethod
    def gene_text(cls, number):
        # num是生成验证码的位数
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的高和宽
        width, height = cls.size
        # 创建图片
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        # 验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text(cls.number)
        # 获取字体尺寸
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        # 绘制干扰线
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        # 绘制噪点
        cls.__gene_points(draw, 10, width, height)
        return (text, image)
"""
