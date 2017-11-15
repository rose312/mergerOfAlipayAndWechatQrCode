# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
import os

from PIL import Image
import qrcode
import zbarlight


# Create your views here.
def index(request):
    contents = {}

    if request.method == 'POST':
        ali = request.FILES.get('ali-img', None)
        wx = request.FILES.get('wx-img', None)
        if ali == None or wx == None:
            return render(request, 'hello/wxcode.html', {'url': None,
                                                         'info': "请先上传微信和支付宝的收款二维码"})

        if ali != None:
            if Img.objects.filter(name='alipay') != None:
                for img in Img.objects.filter(name='alipay'):
                    img.delete()

            nAli_img = Img(
                img=request.FILES.get('ali-img', None),
                name='alipay'
            )
            nAli_img.save()
            # 二维码识别
            file_path = os.path.dirname(os.path.dirname(__file__)) + '/media/'
            result = scanQrCode(file_path + nAli_img.img.name)
            if result != None:
                if result.find('HTTPS://QR.ALIPAY.COM') != -1:
                    print("是支付宝的收款码：" + result[22:])
                    contents['alipay'] = result[22:]
                else:
                    print('不是支付宝收款码')
                    contents['alipay'] = None
                    return render(request, 'hello/wxcode.html', {'url': None,
                                                                 'info': "支付宝收款二维码错误"})
            else:
                print('不是支付宝收款码')
                contents['alipay'] = None
                return render(request, 'hello/wxcode.html', {'url': None,
                                                             'info': "支付宝收款二维码错误"})
            os.remove(file_path + nAli_img.img.name)
        else:
            contents['alipay'] = None
        if wx != None:
            if Img.objects.filter(name='wechat') != None:
                for img in Img.objects.filter(name='wechat'):
                    img.delete()
            nWx_img = Img(
                img=request.FILES.get('wx-img', None),
                name="wechat"
            )
            nWx_img.save()
            # 二维码识别
            file_path = os.path.dirname(os.path.dirname(__file__)) + '/media/'
            result = scanQrCode(file_path + nWx_img.img.name)
            if result != None:
                if result.find('wxp://') != -1:
                    print("是微信的收款码：" + result[6:])
                    contents['wechat'] = result[6:]
                else:
                    print('不是微信收款码')
                    contents['wechat'] = None
                    return render(request, 'hello/wxcode.html', {'url': None,
                                                                 'info': "微信收款二维码错误"})
            else:
                print('不是微信收款码')
                contents['wechat'] = None
                return render(request, 'hello/wxcode.html', {'url': None,
                                                             'info': "微信收款二维码错误"})
            os.remove(file_path + nWx_img.img.name)
        else:
            contents['wechat'] = None
    else:
        contents['alipay'] = None
        contents['wechat'] = None
    print(contents)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if contents['alipay'] != None and contents['wechat'] != None:
        data = 'https://heyfox.herokuapp.com/pay?ali=' + contents['alipay'] + '&wx=' + contents['wechat']
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()

        # LOGO
        logo = request.FILES.get('logo', None)
        if logo != None:
            logo_img = Img(
                img=logo,
                name="logo"
            )
            logo_img.save()
            file_path = os.path.dirname(os.path.dirname(__file__)) + '/media/' + logo_img.img.name
            img = addLogo(img, file_path)
            os.remove(file_path)


        img.save("media/img/qrcode.png")
        file_path = '/media/img/qrcode.png'

        return render(request, 'hello/wxcode.html', {'url': file_path,
                                                     'info': "支持微信和支付宝收款"})
    else:
        return render(request, 'hello/index.html', {'url': None})

def pay(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    print(agent)
    ali = request.GET.get('ali', None)
    wx = request.GET.get('wx', None)
    if ali == None or wx == None:
        return render(request, 'hello/wxcode.html', {'url': None,
                                                     'info': "未知二维码，请重新合成收款二维码"})

    ali = 'HTTPS://QR.ALIPAY.COM/' + ali
    wx = 'wxp://' + wx

    print(ali, wx)

    # MicroMessenger    Alipay
    if str(agent).find('MicroMessenger') != -1:
        print("微信浏览器", wx)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wx)
        qr.make(fit=True)
        img = qr.make_image()
        img.save("media/img/" + request.GET.get('wx', None) + ".png")
        file_path = '/media/img/' + request.GET.get('wx', None) + ".png"
        return render(request, 'hello/wxcode.html', {'url': file_path,
                                                     'info': "长按识别上面的二维码进行支付"})
    elif str(agent).find('Alipay') != -1:
        print('支付宝浏览器', ali)
        return HttpResponseRedirect(ali)
    else:
        return render(request, 'hello/wxcode.html', {'url': None,
                                                     'info': "请使用微信、支付宝进行扫码支付"})


# 添加logo
def addLogo(img, logo):
    try:
        img = img.convert("RGBA")
        icon = Image.open(logo)
        img_w, img_h = img.size
        factor = 6
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img.paste(icon, (w, h), icon)
        return img
    except:
        print('logo添加错误')
        return img


# 二维码识别
def scanQrCode(path):
    # return None
    with open(path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    # wxp://f2f0JV5T664Amfb_JDHLXtMBTrL2_8PvU68O
    # HTTPS://QR.ALIPAY.COM/FKX05639AEMUOSN0TE016F
    codes = zbarlight.scan_codes('qrcode', image)
    if codes != None:
        code = str(codes[0]).lstrip("b'").rstrip("'")
        print('二维码识别结果：' + code)
        return code
    else:
        print('二维码识别失败')
        return None



# zbarlight==1.2
# zbarlight==1.2
# zbar==0.10