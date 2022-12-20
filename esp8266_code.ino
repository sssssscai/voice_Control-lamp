#include <ESP8266WiFi.h>        
#include <WiFiClient.h> 
/*****************网络设置项 *****************/
const char *STAssid ="";                   //需要连接路由器的名称
const char *STApassword="";      //路由器的密码
const char *host= "";              //服务器ip
const int httpPort =;                    //服务器端口
WiFiClient client;                            //声明客户端对象
bool is=0;                                    //用来做连接到服务器后，仅发送一次问候语
int led=14;                                   //灯io，D5
void setup() {
  Serial.begin(115200);
  Serial.println("");
  pinMode(14,OUTPUT);
  digitalWrite(14,0);  
  WiFi.mode(WIFI_STA);                       //设置为STA模式 
  WiFi.begin(STAssid, STApassword);          //配置连接信息，开始连接
  //运行自定义函数，在未连接到路由器的过程中，打印输出......，直到连接成功   
  gotoWifi();  
  Serial.println("连接路由器成功");
  //此时已经连接到路由器，可以开始连接远程服务器   
  lianjie();                                 
}

void loop() {   
/****************检测WiFi连接状态****************/ 
  if (WiFi.status() != WL_CONNECTED) { 
    WiFi.disconnect();
    WiFi.begin(STAssid, STApassword);
    gotoWifi();  
  }
  else{
    if (!client.connected()) {            //如果没有连接到服务器
      lianjie();
      return;
    }
    else{                                //否则，就是连接到服务器
      if(is==0){
        client.print("我是灯泡"); 
        is=1;      
      }
    }
  }
  Tcp_Handler(Read_Tcp());              //读取服务器信息，并处理
}
//读取服务器信息，返回String类型
String Read_Tcp(){
  String data = "";          
  while (client.available() > 0){
    data += char(client.read());
    delay(2);    
  } 
  return data;
}
//处理服务器信息
void Tcp_Handler(String data){
  if(data!=""){
    Serial.print("收到服务器信息：");
    Serial.println(data);
    if(data=="open"){
      digitalWrite(14,0);  
      client.print("open led");     
    }
    else if(data=="close"){
      digitalWrite(14,1); 
      client.print("close led");      
    }
  }  
}
//连接路由器
void gotoWifi(){
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);    
    Serial.print(".");
  }
}
//连接服务器
void lianjie() {
  Serial.println("开始连接服务器");
  client.connect(host, httpPort);
  delay(1000);
}
