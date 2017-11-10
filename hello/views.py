from django.shortcuts import render
from django.http import HttpResponse

from .models import *
import os


# Create your views here.
def index(request):
    contents = {}
    if request.method == 'POST':
        if request.FILES.get('ali-img', None) != None:
            for img in Img.objects.filter(name='alipay'):
                img.delete()

            nAli_img = Img(
                img=request.FILES.get('ali-img', None),
                name='alipay'
            )
            nAli_img.save()
            contents['alipay'] = nAli_img
            print("添加支付宝照片")
        else:
            contents['alipay'] = None
        if request.FILES.get('wx-img', None) != None:
            for img in Img.objects.filter(name='wechat'):
                img.delete()
            nWx_img = Img(
                img=request.FILES.get('wx-img', None),
                name="wechat"
            )
            nWx_img.save()
            contents['wechat'] = nWx_img
            print("添加微信照片")
        else:
            contents['wechat'] = None
    else:
        contents['alipay'] = None
        contents['wechat'] = None
    print(contents)
    print(os.path.dirname(os.path.dirname(__file__)) + '/media/img')
    return render(request, 'hello/index.html', contents)



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