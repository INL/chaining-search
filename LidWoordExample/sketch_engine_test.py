import requests
USERNAME = ''
API_KEY = ''
base_url = 'https://api.sketchengine.eu/bonito/run.cgi'
data = {
 'corpname': 'preloaded/bnc2',
 'format': 'json',
 'lemma': 'book',
 'lpos': '-v',
}
d = requests.get(base_url + '/wsketch?corpname=%s' % data['corpname'], params=data, auth=(USERNAME, API_KEY)).json()
print("There are %d grammar relations for %s%s (lemma+PoS) in corpus %s." % (
    len(d['Gramrels']), data['lemma'], data['lpos'], data['corpname']))


'''
curl 'https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl' \
  -H 'Connection: keep-alive' \
  -H 'Accept: */*' \
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: https://app.sketchengine.eu' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://app.sketchengine.eu/' \
  -H 'Accept-Language: nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2' \
  -H 'Cookie: _ga=GA1.2.876003155.1601996706; _gid=GA1.2.111314773.1610981659; sessionid=dd34fc7c672f4837a7922618b7e5394e; elexisSplashDisplayed=1' \
  --data-raw 'json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A50%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D' \
  --compressed


curl 'https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl' \
  -H 'Connection: keep-alive' \
  -H 'Accept: */*' \
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: https://app.sketchengine.eu' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://app.sketchengine.eu/' \
  -H 'Accept-Language: nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2' \
  -H 'Cookie: _ga=GA1.2.876003155.1601996706; _gid=GA1.2.111314773.1610981659; sessionid=dd34fc7c672f4837a7922618b7e5394e; elexisSplashDisplayed=1' \
  --data-raw 'json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A1000%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D' \
  --compressed


fetch("https://app.sketchengine.eu/texts/en/parc_about.html", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/embed/vklUWMRV1ew", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "upgrade-insecure-requests": "1",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance1.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance2.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-player.css", {
  "headers": {
    "accept": "text/css,*/*;q=0.1",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "style",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-embed-player.vflset/www-embed-player.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/base.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/yts/jsbin/fetch-polyfill-vfl6MZH8P/fetch-polyfill.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://googleads.g.doubleclick.net/pagead/id", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://static.doubleclick.net/instream/ad_status.js", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "if-modified-since": "Thu, 12 Dec 2013 23:40:16 GMT",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.google.com/js/bg/7JZ2fmCMVOl0vw20xI3AsjDeeds-Si0AsriAJ95C_5g.js", {
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/embed.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/generate_204?DxPEHA", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("chrome-extension://mooikfkahbdckldjjndioackbalphokd/assets/prompt.js", {
  "referrer": "",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/youtubei/v1/log_event?alt=json&key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "authorization": "SAPISIDHASH 1610993680_665876f179fe48096503665864332a96a4f4ad43",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "CgtzZXpCUnpiNVB1USiFoJeABg%3D%3D",
    "x-origin": "https://www.youtube.com",
    "x-youtube-ad-signals": "dt=1610993669637&flash=0&frm=2&u_tz=60&u_his=6&u_java&u_h=2160&u_w=3840&u_ah=2116&u_aw=3840&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=-12245933&biw=-12245933&brdim=0%2C0%2C0%2C0%2C3840%2C0%2C3840%2C2116%2C0%2C0&vis=1&wgl=true&ca_type=image&bid=ANyPxKpz9TtqZUP_8RqRRwyCh5IV7N5Da9b7-29XThzlql98niUSJKmoNldeFcy7fwOKSoXMsxnn1QuZsxC5udOwDCT-f_bJ7Q",
    "x-youtube-client-name": "56",
    "x-youtube-client-version": "20210113",
    "x-youtube-time-zone": "Europe/Amsterdam",
    "x-youtube-utc-offset": "60"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"context\":{\"client\":{\"hl\":\"nl\",\"gl\":\"NL\",\"clientName\":56,\"clientVersion\":\"20210113\",\"screenDensityFloat\":\"2\"}},\"events\":[{\"eventTimeMs\":1610993670394,\"screenCreated\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"pageVe\":{\"veType\":16623}},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":51663,\"veCounter\":1}]},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28240,\"veCounter\":2}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28239,\"veCounter\":3}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28240,\"veCounter\":2},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28239,\"veCounter\":3},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36925,\"veCounter\":4}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36926,\"veCounter\":5}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36927,\"veCounter\":6}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":23851,\"veCounter\":7}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28656,\"veCounter\":8}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":70344,\"veCounter\":9}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28665,\"veCounter\":10}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28664,\"veCounter\":11}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":86570,\"veCounter\":12}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":16499,\"veCounter\":13}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":23851,\"veCounter\":7},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}}],\"requestTimeMs\":\"1610993680395\",\"serializedClientEventId\":{\"serializedEventId\":\"BdAFYLOUFYSQgAfjgKDgAQ\",\"clientCounter\":\"1\"}}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A50%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/set_user_options", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22options%22%3A%7B%22user_data_pages_history%5B0%5D%7C__delete%22%3A%22%22%2C%22user_data_pages_history%7C__append%22%3A%7B%22corpname%22%3A%22preloaded%2Fopus2_nl%22%2C%22corpus%22%3A%22OPUS2+Dutch%22%2C%22feature%22%3A%22parconcordance%22%2C%22data%22%3A%7B%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22attrs%22%3A%22word%22%2C%22ctxattrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22page%22%3A1%2C%22itemsPerPage%22%3A50%2C%22linenumbers%22%3A0%2C%22viewmode%22%3A%22align%22%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22attr_allpos%22%3A%22all%22%2C%22tab%22%3A%22advanced%22%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22f_texttypes%22%3A%5B%5D%2C%22freqSort%22%3A%22freq%22%2C%22freqDesc%22%3A%22%22%2C%22showresults%22%3Atrue%2C%22f_itemsPerPage%22%3A10%2C%22glue%22%3A1%2C%22results_screen%22%3A%22concordance%22%2C%22alignedCorpname%22%3A%22%22%2C%22refs_up%22%3A0%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22f_mode%22%3A%22multilevel%22%2C%22f_group%22%3Anull%2C%22gdex_enabled%22%3A0%2C%22gdexcnt%22%3A300%2C%22usesubcorp%22%3A%22%22%2C%22sort%22%3A%5B%5D%7D%2C%22userOptions%22%3A%7B%22iquery%22%3A%7B%22labelId%22%3A%22cc.iquery%22%2C%22value%22%3A%22boek%22%7D%2C%22corpora%22%3A%7B%22labelId%22%3A%22corpora%22%2C%22value%22%3A%22opus2_en%22%7D%7D%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22timestamp%22%3A1610993760342%7D%7D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/translate_kwic?corpname=preloaded/opus2_nl&bim_corpname=preloaded/opus2_en", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json={\"corpname\":\"preloaded/opus2_nl\",\"bim_corpname\":\"opus2_en\",\"data\":\"5479190:1\\t5479193:1\\t5479462:1\\t5498590:1\\t5507431:1\\t5696351:1\\t5720579:1\\t5758525:1\\t5789782:1\\t5790184:1\\t5790254:1\\t5796406:1\\t5796606:1\\t5868130:1\\t5889391:1\\t6006077:1\\t6009228:1\\t6040078:1\\t6044480:1\\t6054196:1\\t6088000:1\\t6099138:1\\t6103316:1\\t6129331:1\\t6177645:1\\t6296037:1\\t6299910:1\\t6299927:1\\t6361294:1\\t6361341:1\\t6361531:1\\t6361982:1\\t6362694:1\\t6373347:1\\t6394805:1\\t6401221:1\\t6401268:1\\t6406190:1\\t6429520:1\\t6450642:1\\t6451271:1\\t6544682:1\\t6596898:1\\t6597876:1\\t6618219:1\\t6618237:1\\t6638148:1\\t6933682:1\\t6934374:1\\t6952454:1\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A1000%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});fetch("https://app.sketchengine.eu/texts/en/parc_about.html", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/embed/vklUWMRV1ew", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "upgrade-insecure-requests": "1",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance1.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance2.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-player.css", {
  "headers": {
    "accept": "text/css,*/*;q=0.1",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "style",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-embed-player.vflset/www-embed-player.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/base.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/yts/jsbin/fetch-polyfill-vfl6MZH8P/fetch-polyfill.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://googleads.g.doubleclick.net/pagead/id", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://static.doubleclick.net/instream/ad_status.js", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "if-modified-since": "Thu, 12 Dec 2013 23:40:16 GMT",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.google.com/js/bg/7JZ2fmCMVOl0vw20xI3AsjDeeds-Si0AsriAJ95C_5g.js", {
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/embed.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/generate_204?DxPEHA", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("chrome-extension://mooikfkahbdckldjjndioackbalphokd/assets/prompt.js", {
  "referrer": "",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/youtubei/v1/log_event?alt=json&key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "authorization": "SAPISIDHASH 1610993680_665876f179fe48096503665864332a96a4f4ad43",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "CgtzZXpCUnpiNVB1USiFoJeABg%3D%3D",
    "x-origin": "https://www.youtube.com",
    "x-youtube-ad-signals": "dt=1610993669637&flash=0&frm=2&u_tz=60&u_his=6&u_java&u_h=2160&u_w=3840&u_ah=2116&u_aw=3840&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=-12245933&biw=-12245933&brdim=0%2C0%2C0%2C0%2C3840%2C0%2C3840%2C2116%2C0%2C0&vis=1&wgl=true&ca_type=image&bid=ANyPxKpz9TtqZUP_8RqRRwyCh5IV7N5Da9b7-29XThzlql98niUSJKmoNldeFcy7fwOKSoXMsxnn1QuZsxC5udOwDCT-f_bJ7Q",
    "x-youtube-client-name": "56",
    "x-youtube-client-version": "20210113",
    "x-youtube-time-zone": "Europe/Amsterdam",
    "x-youtube-utc-offset": "60"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"context\":{\"client\":{\"hl\":\"nl\",\"gl\":\"NL\",\"clientName\":56,\"clientVersion\":\"20210113\",\"screenDensityFloat\":\"2\"}},\"events\":[{\"eventTimeMs\":1610993670394,\"screenCreated\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"pageVe\":{\"veType\":16623}},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":51663,\"veCounter\":1}]},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28240,\"veCounter\":2}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28239,\"veCounter\":3}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28240,\"veCounter\":2},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28239,\"veCounter\":3},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36925,\"veCounter\":4}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36926,\"veCounter\":5}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36927,\"veCounter\":6}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":23851,\"veCounter\":7}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28656,\"veCounter\":8}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":70344,\"veCounter\":9}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28665,\"veCounter\":10}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28664,\"veCounter\":11}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":86570,\"veCounter\":12}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":16499,\"veCounter\":13}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":23851,\"veCounter\":7},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}}],\"requestTimeMs\":\"1610993680395\",\"serializedClientEventId\":{\"serializedEventId\":\"BdAFYLOUFYSQgAfjgKDgAQ\",\"clientCounter\":\"1\"}}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A50%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/set_user_options", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22options%22%3A%7B%22user_data_pages_history%5B0%5D%7C__delete%22%3A%22%22%2C%22user_data_pages_history%7C__append%22%3A%7B%22corpname%22%3A%22preloaded%2Fopus2_nl%22%2C%22corpus%22%3A%22OPUS2+Dutch%22%2C%22feature%22%3A%22parconcordance%22%2C%22data%22%3A%7B%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22attrs%22%3A%22word%22%2C%22ctxattrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22page%22%3A1%2C%22itemsPerPage%22%3A50%2C%22linenumbers%22%3A0%2C%22viewmode%22%3A%22align%22%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22attr_allpos%22%3A%22all%22%2C%22tab%22%3A%22advanced%22%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22f_texttypes%22%3A%5B%5D%2C%22freqSort%22%3A%22freq%22%2C%22freqDesc%22%3A%22%22%2C%22showresults%22%3Atrue%2C%22f_itemsPerPage%22%3A10%2C%22glue%22%3A1%2C%22results_screen%22%3A%22concordance%22%2C%22alignedCorpname%22%3A%22%22%2C%22refs_up%22%3A0%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22f_mode%22%3A%22multilevel%22%2C%22f_group%22%3Anull%2C%22gdex_enabled%22%3A0%2C%22gdexcnt%22%3A300%2C%22usesubcorp%22%3A%22%22%2C%22sort%22%3A%5B%5D%7D%2C%22userOptions%22%3A%7B%22iquery%22%3A%7B%22labelId%22%3A%22cc.iquery%22%2C%22value%22%3A%22boek%22%7D%2C%22corpora%22%3A%7B%22labelId%22%3A%22corpora%22%2C%22value%22%3A%22opus2_en%22%7D%7D%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22timestamp%22%3A1610993760342%7D%7D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/translate_kwic?corpname=preloaded/opus2_nl&bim_corpname=preloaded/opus2_en", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json={\"corpname\":\"preloaded/opus2_nl\",\"bim_corpname\":\"opus2_en\",\"data\":\"5479190:1\\t5479193:1\\t5479462:1\\t5498590:1\\t5507431:1\\t5696351:1\\t5720579:1\\t5758525:1\\t5789782:1\\t5790184:1\\t5790254:1\\t5796406:1\\t5796606:1\\t5868130:1\\t5889391:1\\t6006077:1\\t6009228:1\\t6040078:1\\t6044480:1\\t6054196:1\\t6088000:1\\t6099138:1\\t6103316:1\\t6129331:1\\t6177645:1\\t6296037:1\\t6299910:1\\t6299927:1\\t6361294:1\\t6361341:1\\t6361531:1\\t6361982:1\\t6362694:1\\t6373347:1\\t6394805:1\\t6401221:1\\t6401268:1\\t6406190:1\\t6429520:1\\t6450642:1\\t6451271:1\\t6544682:1\\t6596898:1\\t6597876:1\\t6618219:1\\t6618237:1\\t6638148:1\\t6933682:1\\t6934374:1\\t6952454:1\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A1000%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
})fetch("https://app.sketchengine.eu/texts/en/parc_about.html", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/embed/vklUWMRV1ew", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "upgrade-insecure-requests": "1",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance1.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.sketchengine.eu/wp-content/uploads/parallel-concordance2.png", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-player.css", {
  "headers": {
    "accept": "text/css,*/*;q=0.1",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "style",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/www-embed-player.vflset/www-embed-player.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/base.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/yts/jsbin/fetch-polyfill-vfl6MZH8P/fetch-polyfill.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://googleads.g.doubleclick.net/pagead/id", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://static.doubleclick.net/instream/ad_status.js", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "if-modified-since": "Thu, 12 Dec 2013 23:40:16 GMT",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://www.google.com/js/bg/7JZ2fmCMVOl0vw20xI3AsjDeeds-Si0AsriAJ95C_5g.js", {
  "referrer": "https://www.youtube.com/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/s/player/9f996d3e/player_ias.vflset/nl_NL/embed.js", {
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/generate_204?DxPEHA", {
  "headers": {
    "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("chrome-extension://mooikfkahbdckldjjndioackbalphokd/assets/prompt.js", {
  "referrer": "",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
}); ;
fetch("https://www.youtube.com/youtubei/v1/log_event?alt=json&key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "authorization": "SAPISIDHASH 1610993680_665876f179fe48096503665864332a96a4f4ad43",
    "content-type": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CI62yQEIpLbJAQipncoBCKzHygEI3NXKAQiTmssBCKmdywEIq53LARj6uMoB",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "CgtzZXpCUnpiNVB1USiFoJeABg%3D%3D",
    "x-origin": "https://www.youtube.com",
    "x-youtube-ad-signals": "dt=1610993669637&flash=0&frm=2&u_tz=60&u_his=6&u_java&u_h=2160&u_w=3840&u_ah=2116&u_aw=3840&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=-12245933&biw=-12245933&brdim=0%2C0%2C0%2C0%2C3840%2C0%2C3840%2C2116%2C0%2C0&vis=1&wgl=true&ca_type=image&bid=ANyPxKpz9TtqZUP_8RqRRwyCh5IV7N5Da9b7-29XThzlql98niUSJKmoNldeFcy7fwOKSoXMsxnn1QuZsxC5udOwDCT-f_bJ7Q",
    "x-youtube-client-name": "56",
    "x-youtube-client-version": "20210113",
    "x-youtube-time-zone": "Europe/Amsterdam",
    "x-youtube-utc-offset": "60"
  },
  "referrer": "https://www.youtube.com/embed/vklUWMRV1ew",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"context\":{\"client\":{\"hl\":\"nl\",\"gl\":\"NL\",\"clientName\":56,\"clientVersion\":\"20210113\",\"screenDensityFloat\":\"2\"}},\"events\":[{\"eventTimeMs\":1610993670394,\"screenCreated\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"pageVe\":{\"veType\":16623}},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":51663,\"veCounter\":1}]},\"context\":{\"lastActivityMs\":\"454\"}},{\"eventTimeMs\":1610993670394,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28240,\"veCounter\":2}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28239,\"veCounter\":3}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28240,\"veCounter\":2},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":28239,\"veCounter\":3},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36925,\"veCounter\":4}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36926,\"veCounter\":5}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":36927,\"veCounter\":6}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":23851,\"veCounter\":7}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28656,\"veCounter\":8}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":70344,\"veCounter\":9}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28665,\"veCounter\":10}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":28664,\"veCounter\":11}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":86570,\"veCounter\":12}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementAttached\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"parentVe\":{\"veType\":16623},\"childVes\":[{\"veType\":16499,\"veCounter\":13}]},\"context\":{\"lastActivityMs\":\"455\"}},{\"eventTimeMs\":1610993670395,\"visualElementShown\":{\"csn\":\"MC4xNjU2MzY1MDQzMTM4MjEyNg..\",\"ve\":{\"veType\":23851,\"veCounter\":7},\"eventType\":1},\"context\":{\"lastActivityMs\":\"455\"}}],\"requestTimeMs\":\"1610993680395\",\"serializedClientEventId\":{\"serializedEventId\":\"BdAFYLOUFYSQgAfjgKDgAQ\",\"clientCounter\":\"1\"}}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A50%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/set_user_options", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22options%22%3A%7B%22user_data_pages_history%5B0%5D%7C__delete%22%3A%22%22%2C%22user_data_pages_history%7C__append%22%3A%7B%22corpname%22%3A%22preloaded%2Fopus2_nl%22%2C%22corpus%22%3A%22OPUS2+Dutch%22%2C%22feature%22%3A%22parconcordance%22%2C%22data%22%3A%7B%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22attrs%22%3A%22word%22%2C%22ctxattrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22page%22%3A1%2C%22itemsPerPage%22%3A50%2C%22linenumbers%22%3A0%2C%22viewmode%22%3A%22align%22%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22attr_allpos%22%3A%22all%22%2C%22tab%22%3A%22advanced%22%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22f_texttypes%22%3A%5B%5D%2C%22freqSort%22%3A%22freq%22%2C%22freqDesc%22%3A%22%22%2C%22showresults%22%3Atrue%2C%22f_itemsPerPage%22%3A10%2C%22glue%22%3A1%2C%22results_screen%22%3A%22concordance%22%2C%22alignedCorpname%22%3A%22%22%2C%22refs_up%22%3A0%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22f_mode%22%3A%22multilevel%22%2C%22f_group%22%3Anull%2C%22gdex_enabled%22%3A0%2C%22gdexcnt%22%3A300%2C%22usesubcorp%22%3A%22%22%2C%22sort%22%3A%5B%5D%7D%2C%22userOptions%22%3A%7B%22iquery%22%3A%7B%22labelId%22%3A%22cc.iquery%22%2C%22value%22%3A%22boek%22%7D%2C%22corpora%22%3A%7B%22labelId%22%3A%22corpora%22%2C%22value%22%3A%22opus2_en%22%7D%7D%2C%22operations%22%3A%5B%7B%22name%22%3A%22iquery%22%2C%22arg%22%3A%22boek%22%2C%22active%22%3Atrue%2C%22query%22%3A%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%2C%22id%22%3A5937%7D%5D%2C%22formparts%22%3A%5B%7B%22corpname%22%3A%22opus2_en%22%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%2C%22filter_nonempty%22%3Atrue%2C%22pcq_pos_neg%22%3A%22pos%22%7D%7D%5D%2C%22formValue%22%3A%7B%22queryselector%22%3A%22iquery%22%2C%22keyword%22%3A%22boek%22%2C%22lpos%22%3A%22%22%2C%22wpos%22%3A%22%22%2C%22default_attr%22%3A%22%22%2C%22qmcase%22%3A%22%22%2C%22cql%22%3A%22%22%7D%2C%22timestamp%22%3A1610993760342%7D%7D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/translate_kwic?corpname=preloaded/opus2_nl&bim_corpname=preloaded/opus2_en", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json={\"corpname\":\"preloaded/opus2_nl\",\"bim_corpname\":\"opus2_en\",\"data\":\"5479190:1\\t5479193:1\\t5479462:1\\t5498590:1\\t5507431:1\\t5696351:1\\t5720579:1\\t5758525:1\\t5789782:1\\t5790184:1\\t5790254:1\\t5796406:1\\t5796606:1\\t5868130:1\\t5889391:1\\t6006077:1\\t6009228:1\\t6040078:1\\t6044480:1\\t6054196:1\\t6088000:1\\t6099138:1\\t6103316:1\\t6129331:1\\t6177645:1\\t6296037:1\\t6299910:1\\t6299927:1\\t6361294:1\\t6361341:1\\t6361531:1\\t6361982:1\\t6362694:1\\t6373347:1\\t6394805:1\\t6401221:1\\t6401268:1\\t6406190:1\\t6429520:1\\t6450642:1\\t6451271:1\\t6544682:1\\t6596898:1\\t6597876:1\\t6618219:1\\t6618237:1\\t6638148:1\\t6933682:1\\t6934374:1\\t6952454:1\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}); ;
fetch("https://app.sketchengine.eu/bonito/run.cgi/concordance?corpname=preloaded/opus2_nl", {
  "headers": {
    "accept": "*/*",
    "accept-language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,es;q=0.5,fr;q=0.4,ru;q=0.3,it;q=0.2",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://app.sketchengine.eu/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "json=%7B%22attrs%22%3A%22word%22%2C%22structs%22%3A%22s%2Cg%22%2C%22refs%22%3A%22%3Ddoc.subcorpus%22%2C%22ctxattrs%22%3A%22word%22%2C%22viewmode%22%3A%22align%22%2C%22usesubcorp%22%3A%22%22%2C%22freqml%22%3A%5B%7B%22attr%22%3A%22word%22%2C%22ctx%22%3A%220%22%2C%22base%22%3A%22kwic%22%7D%5D%2C%22glue%22%3A1%2C%22fromp%22%3A1%2C%22pagesize%22%3A1000%2C%22concordance_query%22%3A%5B%7B%22queryselector%22%3A%22iqueryrow%22%2C%22iquery%22%3A%22boek%22%2C%22sel_aligned%22%3A%5B%22opus2_en%22%5D%2C%22queryselector_opus2_en%22%3A%22iqueryrow%22%2C%22iquery_opus2_en%22%3A%22%22%2C%22pcq_pos_neg_opus2_en%22%3A%22pos%22%2C%22filter_nonempty_opus2_en%22%3A%22on%22%7D%5D%7D",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});;
'''
