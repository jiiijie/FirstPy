from bs4 import BeautifulSoup
import urllib.request
import xlwt


# 主函数
def main():
    doubanurl = "https://movie.douban.com/top250?start="
    datalist = getData(doubanurl) # 包含电影数据 调用了getData函数
    savepath = "A豆瓣电影Top250.xls"    # 保存的文件路径
    saveData(datalist, savepath)     # 调用了 saveData 函数 并以datalist和savepath作为参数。

def getData(doubanurl):
    datalist = []   # 用于存储电影数据的列表
    for i in range(0, 10):  # 循环10次，获取前10页的数据
        url = doubanurl + str(i * 25) # 构建当前页面的URL，每页25部电影
        try:
            html = askURL(url)  # 获取当前页面的HTML内容
            soup = BeautifulSoup(html, "html.parser")   # 使用BeautifulSoup解析HTML
            for item in soup.find_all('div', class_="item"):    # 遍历每个电影条目
                data = extractData(item)    # 提取电影数据
                datalist.append(data)   # 将电影数据添加到列表中
        except Exception as e:
            print(f"Error while processing page {url}: {e}")     # 打印异常信息
    return datalist

def askURL(url):
    try:
        headers = { # 定义请求头，模拟浏览器访问
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        # 创建一个Request对象，包含URL和请求头
        request = urllib.request.Request(url, headers=headers)
        # 使用urllib库发送请求并获取响应
        response = urllib.request.urlopen(request)
        # 读取响应的HTML内容，并使用utf-8进行解码
        html = response.read().decode("utf-8")
        # 返回获取到的HTML内容
        return html
    except urllib.error.URLError as e:
        # 如果发生URLError异常，抛出自定义异常并带有错误信息
        raise Exception(f"Failed to fetch data from {url}: {e}")

def extractData(item):
    data = []   # 用于存储提取的电影数据的列表

    # 电影详情链接
    link = item.find('div', class_='hd').a['href']  # 通过查找div标签中class为 'hd' 的子标签的a标签，获取电影详情链接。
    data.append(link)   # 将电影详情链接添加到数据列表中。

    # 图片链接
    imgSrc = item.find('div', class_='pic').img['src']  # 通过查找div标签中class为 'pic' 的子标签的img标签，获取图片链接。
    data.append(imgSrc) # 将图片链接添加到数据列表中

    # 影片中文名和外国名
    title_elements = item.find('span', class_='title').contents # 通过查找span标签中class为 'title' 的子标签的内容，获取包含中文名和外国名的元素列表。
    ctitle = title_elements[0]  # 获取中文名
    otitle = title_elements[1].replace("/", "") if len(title_elements) > 1 else ' ' # 获取外国名，并去除可能的斜杠，如果没有外国名则为空字符串。
    data.append(ctitle) # 将中文名添加到数据列表中
    data.append(otitle) # 将外国名添加到数据列表中

    # 评分
    rating = item.find('span', class_='rating_num').get_text()  #  通过查找span标签中class为 'rating_num' 的子标签，获取评分。
    data.append(rating) # 将评分添加到数据列表中。

    # 评价人数
    star_contents = item.find('div', class_='star').contents    # 通过查找div标签中class为 'star' 的子标签的内容，获取包含评价人数的元素列表。
    judgeNum = star_contents[7].get_text() if len(star_contents) > 7 else ' '   #获取评价人数，并如果没有评价人数则为空字符串。
    data.append(judgeNum)   # 将评价人数添加到数据列表中

    # 概况
    inq = item.find('span', class_='inq')   # 通过查找span标签中class为 'inq' 的子标签，获取概况信息。
    inq_text = inq.get_text(strip=True) if inq else ' ' # 获取概况信息的文本，如果没有概况信息则为空字符串。
    data.append(inq_text)   # 将概况信息添加到数据列表中

    # 相关信息
    bd = item.find('p', class_='').get_text(strip=True) # 通过查找p标签中class为空的子标签，获取相关信息。
    data.append(bd) # 将相关信息添加到数据列表中

    return data # 返回包含提取的电影数据的列表

def saveData(datalist, savepath):
    # 创建一个新的Excel文件（Workbook）对象，指定编码为UTF - 8。
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 在Excel文件中添加一个工作表（Sheet），命名为'豆瓣电影Top250'，cell_overwrite_ok=True表示可以覆盖已有的单元格。
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    #  定义一个包含列名的列表
    col = ["电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价人数", "概况", "相关信息"]
    # 将列名写入Excel表格的第一行
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    # 遍历提取的电影数据列表，enumerate用于同时获取索引和数据。
    for i, data in enumerate(datalist):
        # 将每条电影数据写入Excel表格的相应行中。
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    # 保存Excel文件到指定的路径
    book.save(savepath)

if __name__ == "__main__":
    main()
    print("爬取完毕！")
