import requests,json,re,time,os,sys
S=requests.Session();S.headers['User-Agent']='TripbookBot/1.0 (https://github.com/sujin1537)'
os.makedirs('p',exist_ok=True);cred={}
for line in open('q.txt'):
    if '|' not in line: continue
    k,q=line.strip().split('|',1)
    try:
        r=S.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=q+' filetype:bitmap',gsrnamespace=6,gsrlimit=6,prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=800),timeout=30).json()
        pages=sorted(r.get('query',{}).get('pages',{}).values(),key=lambda x:x['index'])
        ok=False
        for pg in pages:
            ii=pg['imageinfo'][0]
            if ii.get('width',0)<600 or not ii.get('thumburl'): continue
            m=ii.get('extmetadata',{})
            lic=m.get('LicenseShortName',{}).get('value','')
            art=re.sub('<[^>]+>','',m.get('Artist',{}).get('value','')).strip()
            img=S.get(ii['thumburl'],timeout=60)
            if img.status_code!=200: continue
            open(f'p/{k}.jpg','wb').write(img.content)
            cred[k]=dict(title=pg['title'],artist=art[:80],license=lic,url=ii['descriptionurl'])
            print(k,'OK',pg['title'],lic);ok=True;break
        if not ok: print(k,'NONE')
    except Exception as e: print(k,'ERR',e)
    time.sleep(1)
json.dump(cred,open('p/credits.json','w'),ensure_ascii=False,indent=1)
