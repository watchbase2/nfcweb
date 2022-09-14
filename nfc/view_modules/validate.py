import mysql.connector
import urllib.parse
import json
import urllib.request

def getProductInfoFromShopify(jan):

    with open('/etc/nfcweb/shopifyApiKey.txt') as f:
        API_PASSWORD = f.read().strip()
    
    API_VERSION = "2022-01"
    BARCODE = "4589903558390"

    urlString = "https://mybonaventura.myshopify.com/admin/api/" + API_VERSION + "/graphql.json"

    graphql = """
    {
        productVariants(query: "barcode:${BARCODE}", first: 1) {
            edges {
                node {
                    barcode
                    displayName
                    id
                    sku
                    title
                }
            }
        }
    }
    """

    graphql = graphql.replace("${BARCODE}",jan )
    headers = {'content-type': 'application/graphql' , "X-Shopify-Access-Token" : API_PASSWORD}

    try:
        req = urllib.request.Request(url = urlString, headers=headers, method='POST', data=graphql.encode('utf8'))  
        with urllib.request.urlopen(req) as response:body = response.read()

        data = json.loads(body)["data"]
        productVariants = data["productVariants"]
        edges = productVariants["edges"]
        node = edges[0]["node"]
        displayName = node["displayName"]
        variant = node["id"].replace("gid://shopify/ProductVariant/", "")
        sku = node["sku"]
        parent = sku.split("-")[0]

        #print(variant, sku, displayName)

        link = "https://jp.bonaventura.shop/products/" + parent + "?variant=" + variant
        return [displayName, sku, link]
    
    except Exception as e:
        print(e)
        return []


# データベースから指定されたシリアル番号の商品データを取得
def getData(input_sn):
    # Db connection settings
    
    try:
        with open('/etc/nfcweb/dbpassword.txt') as f:
            dbpasswd = f.read().strip()
            
        connection = mysql.connector.connect(
        host='nfc.chvqlhgwnx9k.ap-northeast-1.rds.amazonaws.com',
        user='bona',
        passwd="gmmf8ZFLc9PORTEO",
        database='nfc_dev')
        cursor = connection.cursor()

        sql = "SELECT snumber, uid, jan  FROM master WHERE snumber=%s"
        param = (input_sn,)

        cursor.execute(sql, param)
        for (snumber, uid, jan) in cursor:
            return [snumber, uid, jan]
        
        return []
    except Exception as e:
        print(e)
        #errorHtml()
        print("db error")
        return []

def validateCheck(input_uid, input_sn):
    try:
        result = getData(input_sn)  # [snumber, uid, jan]
        validated = False
        #print(result[0], result[1],result[2])
        
        if result[1] == input_uid:  # uidが同じなので正規品
            validated = True

        jan = result[2]
        info = getProductInfoFromShopify(jan)   # [displayName, sku, link]
        if len(info) > 2:
            info.append(validated)
       
            return info # [ displayName, sku, link, validated]
        return []
    except:
        #errorHtml()
        print("error")
        return []


def showProductPage(input_sn):
    try:
        result = getData(input_sn)
        print(result)
        if len(result) > 2:
            jan = result[2]
            #errorHtml(jan)

            # Shopifyから商品情報を取得
            info = getProductInfoFromShopify(jan)
            if len(info) > 2:
                productUrl = info[2]

                # 取得したURLへリダイレクト
                #print("Location:" + productUrl)
                #print("")     # 何故かこれが必要
                return productUrl
        print("nfc error")
        return ""

    except:
     print("except")
    return ""
#
