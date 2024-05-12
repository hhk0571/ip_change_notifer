<!-- TOC -->

- [介绍](#介绍)
- [第三方软件包](#第三方软件包)
- [使用方法](#使用方法)
    - [设置邮箱信息](#设置邮箱信息)
    - [运行服务程序](#运行服务程序)
    - [配置开机自动执行该程序](#配置开机自动执行该程序)

<!-- /TOC -->

家庭路由器公网IP变化邮件通知器
========

# 介绍
监控家里路由器的公网IP是否发生变化，如果IP变了就发邮件通知我。
我知道有成熟的动态DNS方案，比如花生壳，公云等，所以这个程序之只是写着玩儿 ^_^

# 第三方软件包

安装requests模块, 用于调用RESTful API.
```bash
pip install requests
```

如果需要设置代理才能通过POP3/SMTP收发邮件(比如在公司网络里), 需要安装安装 Pysocks模块:
```bash
pip install Pysocks
```

# 使用方法

## 设置邮箱信息
打开`config.py` 文件进行编辑

因为本程序只用邮件发送功能，只需配置下列信息：
- 接收者邮箱
- IP检测间隔
- smtp服务器/端口
- 用户名/密码
- 代理信息（如果需要的话）

不用设置pop服务器信息，放着不动就好了。

``` python
class Config(object):
    CHECK_INTERVAL = 15 # 检测IP是否变化的间隔，单位为分钟，建议15～30分钟为宜
    RECIEVER     = "xxxx@qq.com"  # 接收者的邮箱
    SMTP_SERVER  = "smtp.163.com" # 发送邮件的服务器
    SMTP_PORT    = 0 # 通常设为0即可, 除非服务器指定使用特殊端口
    ENABLE_SSL   = False # 是否启用SSL, True(是), False(否)
    USERNAME     = "xxxx@163.com" # 邮箱账户名
    PASSWORD     = "xxxx" # 邮箱账户密码 (有些邮箱用的是授权码)
    ENABLE_PROXY = False  # 是否启用代理, True(是), False(否), 如果设为True, 需要配置下面三个参数
    PROXY_TYPE   = 'HTTP' # HTTP, SOCKS4, SOCKS5 三选一, 其中HTTP比较常用
    PROXY_IP     = 'xx.xx.xx.xx' # 代理IP地址
    PROXY_PORT   = 8080 # 代理端口
    DEBUG_LEVEL  = 0 # 0 - disable, 1 - enable
```

## 运行服务程序
在家里的计算机（最好是Linux，比如Ubuntu，在Windows上也可以）上运行服务程序, 执行的命令如下:
```bash
python3 ip_change_notifer.py
```

如需取消, 请按 `CTRL+C`

## 配置开机自动执行该程序

### 编辑service文件

hhk_ip_change_notifer.service:
```bash
# 根据自己的程序存放路径设置service文件里到工作目录
WorkingDirectory=/home/hhk/projects/ip_change_notifer
```
### 安装service

```bash
sudo cp hhk_ip_change_notifer.service /lib/systemd/system/

# 启动service
sudo systemctl start hhk_ip_change_notifer.service

# 激活service (使service在开机时自动启动)
sudo systemctl enable hhk_ip_change_notifer.service

# 查看service状态
sudo systemctl status hhk_ip_change_notifer.service
```
