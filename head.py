from fake_useragent import UserAgent
ua = UserAgent()

headers = [{
    'authority': 'vsco.co',
    'dnt': '1',
    'x-client-platform': 'web',
    'content-type': 'application/json',
    'user-agent': ua.random,
    'x-client-build': '1',
    'accept': '*/*',
    'referer': 'https://vsco.co/{}/gallery',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}, {
    'authority': 'vsco.co',
    'cache-control': 'max-age=0',
    'authorization': 'Bearer {}',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': ua.random,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'if-none-match': 'W/"1c3f4-kskXLcbdUJIZ38aJCbwJJsHDftk"',
}]