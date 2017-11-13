from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
import os

from PIL import Image
import qrcode
# import zbarlight

# Create your views here.
def index(request):
    contents = {}

    if request.method == 'POST':
        ali = request.FILES.get('ali-img', None)
        wx = request.FILES.get('wx-img', None)
        if ali == None or wx == None:
            return HttpResponse("请上传微信和支付宝收款二维码")

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
                    print("是支付宝的收款码：" + result)
                    contents['alipay'] = result
                else:
                    print('不是支付宝收款码')
                    contents['alipay'] = None
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
        img.save("media/img/qrcode.png")
        file_path = '/media/img/qrcode.png'
        return render(request, 'hello/index.html', {'url': file_path})
    else:
        data = 'https://heyfox.herokuapp.com/pay?ali=' + 'alipayaaaa' + '&wx=' + 'dafadfafa'
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        img.save("media/img/qrcode.png")
        file_path = '/media/img/qrcode.png'
        return render(request, 'hello/index.html', {'url': file_path})

def pay(request):
    agent = request.META.get('HTTP_USER_AGENT', None)
    print(agent)
    ali = request.GET.get('ali', None)
    wx = request.GET.get('wx', None)
    if ali == None or wx == None:
        return HttpResponse('二维码信息错误')

    ali = 'HTTPS://QR.ALIPAY.COM/' + ali
    wx = 'wxp://' + wx

    print(ali, wx)

    # MicroMessenger    Alipay
    if str(agent).find('MicroMessenger') != -1:
        print("微信浏览器", wx)
        return HttpResponse('微信扫码', wx)
    elif str(agent).find('Alipay') != -1:
        print('支付宝浏览器', ali)
        return HttpResponseRedirect(ali)
    else:
        return HttpResponse('请使用微信或者支付宝扫码')


# 二维码识别
def scanQrCode(path):
    # with open(path, 'rb') as image_file:
    #     image = Image.open(image_file)
    #     image.load()
    # # wxp://f2f0JV5T664Amfb_JDHLXtMBTrL2_8PvU68O
    # # HTTPS://QR.ALIPAY.COM/FKX05639AEMUOSN0TE016F
    # codes = zbarlight.scan_codes('qrcode', image)
    # if codes != None:
    #     code = str(codes[0]).lstrip("b'").rstrip("'")
    #     print('二维码识别结果：' + code)
    #     return code
    # else:
    #     print('二维码识别失败')
    #     return None
    return None
