import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from downloader import Downloader
import csv


class MemologoSpider(CrawlSpider):
    name = "memologo"
    

    def createFile(self):
        with open('urls.csv', mode='w') as file:
            fieldnames = ['url', 'likes']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    def appendRow(self, url, likes):
        with open('urls.csv', mode='a') as file:
            writer = csv.writer(file, delimiter = ",", quotechar='"', quoting = csv.QUOTE_MINIMAL)
            writer.writerow([url,likes])

    #en esta funcion se hace el inicio de sesion, devulve el html y las cookies (session handling)
    def start_requests(self):
        self.createFile()
        url = "https://www.instagram.com"
        script = '''
        function main(splash, args)
  
        splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")

        splash:init_cookies(splash.args.cookies)

        assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        
        local user = splash:select('input[name=username]')
        user:send_text("user")
        splash:wait(0.5)
        
        local pass = splash:select('input[name=password]')
        pass:send_text("pass")
        splash:wait(0.5)
        local button = splash:select('button[type=submit]')
        button.click()
        splash:wait(5)
        
        assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
        assert(splash:wait(5))
        
        return {
            html = splash:html(),
            cookies = splash:get_cookies()
        }
        end
    '''
        yield SplashRequest(url, 
                            self.getUrls,
                            args={'lua_source': script},
                            endpoint='execute',
                            cache_args=['lua_source']    
                            )

    #va al instagram objetivo para obetener las imagenes
    def getUrls(self, response):
        script = """
            function main(splash)
            splash:init_cookies(splash.args.cookies)
            assert(splash:go(splash.args.url))
            assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
            assert(splash:wait(0.5))
            splash:set_viewport_full()
            assert(splash:wait(2))

            return {
                cookies = splash:get_cookies(),
                html = splash:html()
            }
          end

        """
        #print("--------------------------------------")
        #img = Selector(text=response.data['html']).xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/div[1]/div[1]/img/@src').extract()
        #print(img)
        ##url = Selector(text=response.data['html']).xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/@href').extract() 
        #container = Selector(text=response.data['html']).xpath("//div[@class='eLAPa']/div/img/@src").extract()
        #print (container)

        yield SplashRequest(
            url='https://www.instagram.com/purowebeoo/',
            callback=self.interactions,
            endpoint='execute',
            cookies = response.data['cookies'],
            args={'lua_source': script},
        )

    #va a cada una de las imagenes tomadas anteriormente
    def interactions(self, response):
        #urls = Selector(text=response.data['html']).xpath('//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/@href').extract()
        script = """
            function main(splash)
            splash:init_cookies(splash.args.cookies)
            assert(splash:go(splash.args.url))
            assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
            assert(splash:wait(3))
            splash:set_viewport_full()
            assert(splash:wait(3))

            return {
                cookies = splash:get_cookies(),
                html = splash:html()
            }
          end
        """
        
        rawUrls = Selector(text=response.data['html']).xpath('//div[contains(@class,"v1Nh3")]/a/@href').extract()
        urls = []
        for url in rawUrls: 
            urls.append("https://www.instagram.com" + url)

        print(urls)

        for url in urls:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                endpoint='execute',
                cookies = response.data['cookies'],
                args={'wait': 3,
                    'lua_source': script},
            )
        

    #extrae los likes de cada imagen 
    def parse(self, response):
        #print(response.url)
        #print("download")
        #down = Downloader()
        #down.download("https://instagram.fscl13-2.fna.fbcdn.net/v/t51.2885-15/e35/150558941_268689594630299_2984484207877931746_n.jpg?_nc_ht=instagram.fscl13-2.fna.fbcdn.net&_nc_cat=1&_nc_ohc=Ug0GSXompeUAX9h6t3p&tp=1&oh=761d3ca46f856b17c9a4108d3d8b1bef&oe=6055F56F")

        try:
            likes = Selector(text=response.data['html']).xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/a/span/text()').extract()[0]
            self.appendRow(response.url, likes)
        except:
            print("no se pudo obetener los likes")


    
        
        
        