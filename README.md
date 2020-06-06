# django_local_library
Local Library website written in Django

# Quick start

要启动本项目在本地电脑上运行：

1. 克隆此项目到本地并进入文件夹

    ```bash
    git clone git@github.com:yyxiaowei/django_local_library.git
    cd django_local_library
    ```

    

2. 设置`Python`开发环境，推荐使用虚拟环境。（如果你使用的是Windows,则可以使用py或py-3代替python来启动`Python`），请运行以下命令

    ```bash
    python3 -m venv venv
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser # 创建一个超级用户
    python manage.py runserver
    ```

3. 打开浏览器窗口并输入 <http://127.0.0.1:8000/admin/>进入`Django`管理站点
4. 添加生成一些测试数据
5. 输入<http://127.0.0.1:8000/catalog/>>在网页查看生成的数据

