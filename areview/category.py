#category fields#

def aid_context():
    photo_url=["https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Paris_RER_A_icon.svg/1024px-Paris_RER_A_icon.svg.png",
               "https://www.freeiconspng.com/uploads/-20-mb-format-psd-color-theme-blue-white-keywords-information-icon-2.jpg",
               "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Paris_RER_D_icon.svg/1022px-Paris_RER_D_icon.svg.png" ]
    photo_url.reverse()
    category={'분석':'Analysis','통찰력':'Insight','데이터':'Data'}
    return ({'category':category,'photo_url':photo_url})



def study_context():
    photo_url= ['upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/2000px-Python-logo-notext.svg.png',
                'image.freepik.com/free-icon/mathematical-operations_318-35768.jpg',
                'cdn-images-1.medium.com/max/1600/1*1OBwwxzJksMv0YDD-XmyBw.png',
                'cdn4.iconfinder.com/data/icons/web-app-flat-circular-icons-set/64/Iconos_Redondos_Flat_Estadisticas_Icn-512.png']
    photo_url.reverse()
    category={'파이썬':'Python','수학':'Mathmatics','장고':'Diango','통계':'Statistics'}
    return ({'category':category,'photo_url':photo_url})


def project_context():
    photo_url= ['51pC%2BwU6IZL.jpg','71VxcMnuWxL._SX679_.jpg','718i4jG9n2L._SY450_.jpg','71HavoERfhL._UX385_.jpg',
                '917y2jvjjZL._SX466_.jpg','71JTHffuDOL._UX679_.jpg','51unaKlEuWL.jpg','51nIkzdA3IL._SY355_.png',
                '71Fxmk2GAYL._UY445_.jpg','81Eq0-Yx1oL._UY679_.jpg','91qdE638dxL._SY450_.jpg', '71Ikuq6AAfL._SY550_.jpg']
    photo_url.reverse()
    category={'핸드폰':'Cellphone','베개':'Pillow','컴퓨터 마우스':'Mouse','비니 모자':'Beanie','아령':'Dumbell',
              '치마':'Skirt','치약':'Toothpaste','음악':'Music','손목시계':'Watch','맨투맨':'SweatShirt',
              '여행가방':'Luggagebag','커피머신':'Coffeemachine'}
    return ({'category':category, 'photo_url':photo_url})


def contact_context():
    photo_url= ['bellebnb.com/blog/img/9-facebook-icon.svg',
                'instagram-brand.com/wp-content/uploads/2016/11/app-icon2.png',
                'www.logobee.com/uploads/twitter-icon.jpg',
                'vinoaj.com/wp-content/uploads/2017/11/gmail-icon.png']
    photo_url.reverse()
    category={'페이스북':'Facebook','인스타그램':'Instagram','트위터':'Twitter','G메일':'GMail'}
    return ({'category':category,'photo_url':photo_url})


