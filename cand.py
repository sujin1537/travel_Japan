import requests,json,re,time,os
S=requests.Session();S.headers['User-Agent']='TripbookBot/1.0 (https://github.com/sujin1537)'
os.makedirs('c',exist_ok=True);meta={}
Q={'kusatsu':'Kusatsu Onsen Yubatake','ginzan':'Ginzan Onsen','shirakawa':'Shirakawa-go gassho','gero':'Gero Onsen'}
for k,q in Q.items():
    r=S.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=10,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1000),timeout=30).json()
    pages=sorted(r.get('query',{}).get('pages',{}).values(),key=lambda x:x['index'])
    n=0
    for pg in pages:
        ii=pg['imageinfo'][0]
        if ii.get('width',0)<800 or ii.get('width',0)<ii.get('height',1) or not ii.get('thumburl'): continue
        m=ii.get('extmetadata',{})
        img=S.get(ii['thumburl'],timeout=60)
        if img.status_code!=200: continue
        open(f'c/{k}_{n}.jpg','wb').write(img.content)
        meta[f'{k}_{n}']=dict(title=pg['title'],artist=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','')).strip()[:80],license=m.get('LicenseShortName',{}).get('value',''),url=ii['descriptionurl'])
        n+=1;time.sleep(.5)
        if n>=5:break
json.dump(meta,open('c/meta.json','w'),ensure_ascii=False,indent=1)
