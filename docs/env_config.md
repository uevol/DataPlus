### 开发环境搭建(python3)

#### 1. 安装python3
    安装依赖包
    yum -y groupinstall "Development tools"
    yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
  
    下载python3二进制文件
    curl -O https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz

    解压压缩包并安装
    mkdir /usr/local/python3
    tar -xvJf  Python-3.6.2.tar.xz
    cd Python-3.6.2
    ./configure --prefix=/usr/local/python3
    make && make install
    
    最后创建软链接
	ln -s /usr/local/python3/bin/python3 /usr/bin/python3
	ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
    
#### 2. 修改pip3官方源为豆瓣源
    mkdir ~/.pip
    vi ~/.pip/pip.conf
    [global]
    index-url = http://pypi.douban.com/simple
    trusted-host = pypi.douban.com

#### 2. 安装virtualenv

    pip install virtualenv
    ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv

#### 3. 安装git
    yum -y install git

#### 4. 新建python3开发环境
    virtualenv 

#### 5. 安装mysql
    安装软件包
    rpm -ivh https://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
    yum install mysql-community-server -y

    启动mysql
    service mysqld start

    设置root用户密码
    grep 'temporary password' /var/log/mysqld.log
    mysql -u root -p temporary password
    修改root用户的密码：
    ALERT USER 'root'@'localhost' IDENTIFIED BY 'R00t@123';

    设置开机启动
    systemctl enable mysqld

#### 6. 安装django
    pip3 install django

#### 7. 安装MySQL数据库python
    pip3 install PyMySQL

#### 8. 为应用建开发数据库
    create database dataPlus default charset=utf8;
    grant all on dataPlus.* to dataPlus@'%' identified by "xxxxx";
