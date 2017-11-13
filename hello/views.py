from django.shortcuts import render
from django.http import HttpResponse

from .models import *
import os

import pytesseract
from PIL import Image
import qrcode
import zbarlight

# Create your views here.
def index(request):
    contents = {}
    if request.method == 'POST':
        if request.FILES.get('ali-img', None) != None:
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
                    print("是支付宝的收款码：" + result)
                    contents['alipay'] = result
                else:
                    print('不是支付宝收款码')
                    contents['alipay'] = None
            os.remove(file_path + nAli_img.img.name)
        else:
            contents['alipay'] = None
        if request.FILES.get('wx-img', None) != None:
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
                    print("是微信的收款码：" + result)
                    contents['wechat'] = result
                else:
                    print('不是微信收款码')
                    contents['wechat'] = None
            os.remove(file_path + nWx_img.img.name)
        else:
            contents['wechat'] = None
    else:
        contents['alipay'] = None
        contents['wechat'] = None
    print(contents)
    # print(os.path.dirname(os.path.dirname(__file__)) + '/media/img')


    return render(request, 'hello/index.html', contents)

# 二维码识别
def scanQrCode(path):
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

def uploadImg(reqest):
    print("ssssss")
    return HttpResponse('hddd')
    # if request.method == 'POST':
    #     WxImg.objects.all().delete()
    #     new_img = WxImg(
    #         img = request.FILES.get('img'),
    #         name = request.FILES.get('img').name
    #     )
    #     new_img.save()
    #     print("上传成功")
    # return render(request, 'hello/upload.html')