from setuptools import setup,find_packages

setup(
    name = 'Somendra_STT',
    version = '1.0',
    author = 'Somendra Kumar Yadav',
    author_email = 'ysomendra901@gmail.com',
    description='This Speech To Text Module is developed by SOMENDRA KUMAR YADAV',

)
packages = find_packages()
install_requirements = [
    'selenium'
    'webdriver_manager'
]