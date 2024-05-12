class Config(object):
    CHECK_INTERVAL = 15 # 检测IP是否变化的间隔，单位为分钟，建议15～30分钟为宜
    RECIEVER     = "xxxx@qq.com"  # 接收者的邮箱
    SMTP_SERVER  = "smtp.163.com" # 发送邮件的服务器
    SMTP_PORT    = 0 # 通常设为0即可, 除非服务器指定使用特殊端口
    ENABLE_SSL   = False # 是否启用SSL, True(是), False(否)
    USERNAME     = "xxxx@163.com" # 邮箱账户名
    PASSWORD     = "xxxx" # 邮箱账户密码 (有些邮箱用的是授权码)
    ENABLE_PROXY = False # 是否启用代理, True(是), False(否), 如果设为True, 需要配置下面三个参数
    PROXY_TYPE   = 'HTTP' # HTTP, SOCKS4, SOCKS5 三选一, 其中HTTP比较常用
    PROXY_IP     = 'xx.xx.xx.xx' # 代理IP地址
    PROXY_PORT   = 8080 # 代理端口
    DEBUG_LEVEL  = 0 # 0 - disable, 1 - enable
