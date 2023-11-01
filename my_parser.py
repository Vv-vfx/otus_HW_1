from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import requests, json

class MyParser:
    
    def parse_links_on_page(self, url):
        """получаю список всех аюсолютных ссылок с указанного url """
        
        # Получаю базовый url
        parsed_url = urlparse(url)
        base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        
        # Получаю ссылки
        responсe = requests.get(url)
        soup = bs(responсe.text, 'html.parser')
        links = [link['href'] for link in soup.find_all('a')]
        
        # Превращаю относительные ссылки в абсолютные
        absolute_links_on_page = []
        for link in links:
            if urlparse(link).netloc:
                absolute_links_on_page.append(link)
            else:
                absolute_links_on_page.append(f'{base_url}://{link}')
       
        # уменьшаю список ссылок до пяти чтобы не ждать долго
        return absolute_links_on_page[:5]
            
    
    def print_base_links_in_terminal(self, link):
        """ Выводим ссылки с указанной страницы в терминал"""
        
        print("Собираем данные...")

        for link in self.parse_links_on_page(link):
            print(link)
            
        print("Готово")

    def save_base_links_to_file(self, link):
        """ Выводим ссылки с указанной страницы в файл links.txt"""
        
        print("Собираем данные...")
        
        with open("links.json", "w") as file:
            json.dump(self.parse_links_on_page(link), file)   
            file.close()         
        
        print("Готово")
    
    def recursion_links(self, link, /, mode):
        """ Выводим все ссылки из каждой ссылки указанной страницы в терминал
        или в файл
        
        mode:
        "terminal" - в терминал \n
        "file" - в файл
        """
        
        if mode not in ("terminal", "file"):
            raise ValueError(f"Не правильное значение для mode (terminal, file)")
            
        print("Собираем данные...")
        
        dict_links = {}
        
        for link in self.parse_links_on_page(link):
                
                # проверяем ссылку на валидность
                try:
                    responce = requests.get(link)
                except:
                    continue
                
                if responce.status_code == 200:
                    dict_links[link] = self.parse_links_on_page(link)
        
        if mode == 'terminal':
            print(dict_links)
        else:
            with open("links.json", "w") as file:
                json.dump(dict_links, file)   
                file.close()
        
        print("Готово")

     
parser = MyParser()

link = "https://plotegor.medium.com/best-multi-links-services-fea6d2208c0a"

parser.print_base_links_in_terminal(link)
# parser.save_base_links_to_file(link)
# parser.recursion_links(link, mode='terminal')
# parser.recursion_links(link, mode='file')

