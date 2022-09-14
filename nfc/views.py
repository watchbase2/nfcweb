from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect

from  nfc.view_modules import validate
    
class IndexView(TemplateView):
    def get(self, request, uid, sn):    # URLパラメータを受け取る
        params = {'uid': uid, 'sn':sn }
        return render(request, 'index.html', params)
    
class Error(TemplateView):
    def get(self, request):
        return render(request, 'error.html')
            
class Validate(TemplateView):

    def post(self,request):
        #　index.htmlのFormから受け取る
        uid = request.POST["uid"]
        sn = request.POST["sn"]
        mode = request.POST["mode"]
        
        if mode == "validate":
            # 真贋チェック
            info = validate.validateCheck(uid, sn)    # [validated, displayName, sku, link]
            if len(info) > 3:
                product_name = info[0]
                sku = info[1]
                productPage = info[2]
                validated = info[3]

                params = {'uid': uid, 'snumber':sn , 'product_name':product_name, 'sku':sku, 'validated':validated, 'productPage':productPage}
                return render(request, 'validate_result.html', params)
            else:
                return render(request, 'error.html')
            
        else:
            # 商品ページを表示
            productUrl = validate.showProductPage(sn)
            print("show product")
            if productUrl != "":
                return redirect( productUrl)

            print("product url is blank")
            return render(request, 'error.html')