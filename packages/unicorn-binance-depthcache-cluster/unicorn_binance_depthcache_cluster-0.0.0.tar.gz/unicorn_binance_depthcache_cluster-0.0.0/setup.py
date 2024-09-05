from setuptools import setup, find_packages

file_path = "dummy/name.txt"

with open(file_path, 'r') as file:
    package_name = file.read().strip()

setup(
     name=package_name,
     version='0.0.0',
     author="LUCIT Systems and Development",
     author_email='info@lucit.tech',
     url=f"https://github.com/LUCIT-Systems-and-Development/{package_name}",
     description="",
     long_description="",
     long_description_content_type="text/markdown",
     license='LSOSL - LUCIT Synergetic Open Source License',
     install_requires=[],
     keywords='',
     project_urls={
        'Author': 'https://www.lucit.tech',
        'Telegram': 'https://t.me/unicorndevs',
        'Get Support': 'https://www.lucit.tech/get-support.html',
        'LUCIT Online Shop': 'https://shop.lucit.services/software',
     },
     python_requires='>=3.7.0',
     packages=find_packages(exclude=["tools", "images", "dev", "docs", ".github"]),
     classifiers=[
         "Development Status :: 1 - Planning",
         "Programming Language :: Python",
     ],
)
