# voice_Control-lamp
期末项目

该项目实现了一套声控电灯的系统。

使用了百度的语音识别技术，电灯连接的开发板为esp8266

使用时需要注意以下问题:
1.esp8266和客户端连接同一网络，并在命令提示符中输入ipconfig获取无线局域网适配器的ipV4地址
2.将esp8266的烧录代码中，修改自己的路由器名称密码，服务器ip以及端口号
3.修改main中的自己的BAIDU_APP_ID，BAIDU_API_KEY，BAIDU_SECRET_KEY 
4.修改main中的ip地址为1中所查询的
5.先运行tcp_server.py建立服务器，之后电灯通电连接服务器后在运行main.py,如一切正常则会显示ui交互界面
