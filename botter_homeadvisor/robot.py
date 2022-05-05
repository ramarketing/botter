from selenium.webdriver.common.by import By

from botter_base import RobotBase


class RobotHomeAdvisor(RobotBase):
    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def handle(self):
        self.driver = self.get_driver(size=(1200, 700))
        self.do_login()
        links = []

        while len(links) == 0:
            self.go_to_oportunities()
            links = self.get_list_items()

        for link in links:
            content = self.get_link_data(link)
            self.send_to_service(content)
        self.wait(10)

    def do_login(self):
        self.driver.get('https://pro.homeadvisor.com/login?execution=e1s1')
        self.fill_input(By.ID, 'username', self.username)
        self.fill_input(By.ID, 'password', self.password)
        self.click_element(By.CSS_SELECTOR, 'input[type="submit"]')

    def go_to_oportunities(self):
        self.driver.get('https://pro.homeadvisor.com/opportunities/')
        self.wait(5)

    def get_list_items(self):
        elements = self.get_elements(By.CSS_SELECTOR, 'a.lead-card-link')
        response = []

        for element in elements:
            link = element.get_attribute('href')
            link = link.replace('/opportunities/details/OL/', '/ols/lead/')
            if not link.startswith('http'):
                link = f'https://pro.homeadvisor.com{link}'
            response.append(link)
        return response

    def get_link_data(self, link):
        self.driver.get(link)
        content = self.get_element(By.ID, 'jsonModel')
        return content.get_attribute('innerHTML')

    def send_to_service(self, content):
        pass
