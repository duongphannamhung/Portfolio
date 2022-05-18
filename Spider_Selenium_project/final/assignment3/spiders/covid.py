from doctest import DocTestFailure
import scrapy
import logging
import re
import json

# Add thêm source code bỏ các dấu tiếng Việt
def no_accent_vietnamese(s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        marks_list = [u'\u0300', u'\u0301', u'\u0302', u'\u0303', u'\u0306',u'\u0309', u'\u0323']
        for mark in marks_list:
            s = s.replace(mark, '')
        return s

class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20210907023426/https://ncov.moh.gov.vn/vi/web/guest/dong-thoi-gian']    

    def parse(self, response):
        # Xpath chứa nút chuyển trang
        pages = response.xpath('//div[@class="clearfix lfr-pagination"]')
        # Thay vì dùng một function khác để chạy thì chuyển vào chung luôn hàm này và loop qua các trang (một phần vì không cần dùng meta để lấy text tại nút chứa hyperlink như ví dụ)
        for page in pages:
            # Xpath gồm từng timeline chứa từng nội dung của mỗi ngày
            timelines = response.xpath('//div[@class="timeline-detail"]')
            for timeline in timelines:
                # Trong timeline lấy phần thời gian của thông tin
                time = timeline.xpath('.//div/h3/text()').get()
                # Trong timeline lấy phần text chứa số ca tổng của ngày (dùng hàm chuyển từ Vietnamese -> không dấu)
                new_case = no_accent_vietnamese(timeline.xpath('.//div[2]/p[2]/text()').get())
                regex = "[0-9]+(?= CA)"
                # Dùng regex để tách lấy số lượng trong new_case
                new_case=int(re.findall(regex, new_case)[0])

                # (Phần nâng cao) Lấy phần xpath của điểm báo số ca mỗi thành phố. Dùng regex để tách tên thành phố sau đó đến tách số. 
                detail = no_accent_vietnamese(timeline.xpath('.//div[2]/p[3]/text()').get())
                regex_city = '((?: [A-Z][a-z]+)+)(?= \([0-9])'
                city =  re.findall(regex_city, detail)

                regex_case = '(?<=\()[\.,\d]+(?=\))'
                case = re.findall(regex_case, detail)

                # Dùng hàm json để dump vào dạng json theo yêu cầu đề bài, ở đây có a[1:] là vì tên thành phố được lấy ở phía trên bị dư ra một dấu cách nên chỉ lấy phần sau vị trí này của string
                city_case = json.dumps([{'city':a[1:],'case':b} for a,b in zip(city,case)])

                # Parsing
                yield {
                    'time' : time,
                    'new_case': new_case,
                    'city_case': city_case
                }
            
            # Lấy link href từ phần xpath chứa nút chuyển trang. Sau đó follow link để chuyển sang trang tiếp sau khi parse xong một trang
            link = page.xpath(".//ul/li[2]/a/@href").get()
            yield response.follow(url=link)