from setuptools import setup, find_packages


setup(
   name='funpay-cfn',  # Вставьте уникальное имя вашей библиотеки
   version='0.1.2',
   author='cfn',
   author_email='cfn@cfn.com',
   description='cfn',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   packages=find_packages(),
   install_requires=[
       'requests_toolbelt',
       'beautifulsoup4',
       'requests',
   ],
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   python_requires='>=3.6',
)