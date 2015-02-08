# theta_hack
theta_hack for cicp project

##目次  　
１．ThetaカメラをPythonで制御する  
２．JPEGのexifデータをpythonで解析する  
３．Raspberry PiからGPSデータを取得する  
４．GPSデータを解析  
５．統合作業  
６．おまけ  

##１．ThetaカメラをPythonで制御する  
まず，Thetaカメラは電源をONにすると，アクセスポイントとして振る舞います．  
そして，通常はTheta本体が192.168.1.1，そしてThetaに接続した端末が192.168.1.5に設定されます．  
1台以上の端末を同時に接続することは不可能みたいです．  

Thetaカメラと端末はPTP/IP通信をおこないます．  
PTP/IPとは，画像を送信するためのプロトコルみたいです．  
PTPはPicture Transfer Protcolです．  

以下のサイトに，PythonでThataカメラをハックした方のコードがのっています．  
参照サイト：https://gist.github.com/tako2/7734472  
あらかじめThetaカメラにwifi接続して，このプログラムを実行すると，  
シャッターを切って，画像を落としてくれます．  

##２．JPEGのexifデータをpythonで解析する  
あとは，取得した画像のexifデータを解析して，GPSデータを抽出すればOKなはずだが...  
実は，それは大きな間違いでした．  

今回，pythonのライブラリでExifReadというものを発見しました．  
これを使用すると一発で，Exifデータを解析してくれます．  
参照サイト：https://pypi.python.org/pypi/ExifRead  
ただ，何回とってもGPSデータが空白で，有用なデータが取得できない．  

で，いろいろ調べていると，なんと！！実はThetaにはGPSが搭載していないことに気づきました．  
GPSのデータは，あくまでスマホアプリから撮影した時の，スマホのGPS情報を付加させているだけのようです．  

##３．Raspberry PiからGPSデータを取得する
でも，今回ファントムをトラッキングするために，GPS情報が必要なので，  
Raspberry Pi　A+にGPSモジュールを接続したものをファントムに搭載することに決定しました！！  

つまり，Raspberry　Piですべての制御とセンシングを行います．  
Thetaの撮影を一定間隔で行いながら，GPSのデータを取得して，そのデータを溜めていくような構成です．  

今回，使用したGPSモジュールは「GPS Module PMB-648」  
仕様は，こんな感じです．  
- Power requirements: 3.3 to 5 VDC  
- Power consumption: 65 mA @ 5 VDC  
- Communications: TTL or RS-232 asynchronous serial @ 4800 bps  
- Supported NMEA sentences: GGA, GSV, GSA, RMC (optional VTG, GLL)  
- Dimensions: 1.25 x 1.25 x .35 in (32 x 32 x 9 mm)  

Raspberry PiとUART，シリアル通信  
Raspberry　Pi上でシリアル通信をする場合，以下の初期設定をする必要がある．  

参照サイト：http://nanicananica.blog.fc2.com/blog-entry-14.html  

1-1./boot/cmdline.txtの修正  
　念のため、バックアップを取りました  
　$ sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt  
その後に、実際に修正します。  
　$ sudo nano /boot/cmdline.txt  

　　dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait  
　　↓  
　　dwc_otg.lpm_enable=0 rpitestmode=1 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait  

　　削除　：　console=ttyAMA0,115200 kgdboc=ttyAMA0,115200  
　　追加　：　rpitestmode=1  

1-2.再起動  
　　$ sudo reboot  

1-3./etc/inittabを編集  
　こちらも念のため、バックアップを取りました  
　$ sudo cp /etc/inittab /etc/inittab_backup.txt  
その後に、実際に修正します。  
　$ sudo nano /etc/inittab  

　一番最後の行のttyAMA0の行をコメントアウトします  
　　T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100  
　　↓  
　　#T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100  

1-4.再起動  
　もう一度再起動して完了  

Raspberry Pi上のターミナルでシリアル通信を簡単に行うために，便利なツールがminicomです．  
sudo apt-get install minicom  
minicom -b 4800-o -D /dev/ttyAMA0  
で通信を確認することが出来ます．  

今回は，pythonのスクリプトを作って通信を確認しました．  
python  
import serial (pip install pySerial必須)  
ser = serial.Serial('/dev/ttyAMA0',4800)  
for line in itre(ser.readline(),’\n’):  
     print (line.rstrip())  

##４．GPSデータを解析  
出力された結果が，  
$GPRMC,000721.036,V,0000.0000,N,00000.0000,E,,,150209,,,N*78  
$GPGGA,000722.036,0000.0000,N,00000.0000,E,0,00,,0.0,M,0.0,M,,0000*41  
$GPGSA,A,1,,,,,,,,,,,,,,,*1E  
上記データの繰り返し．  
調べてみると，どうやらNMEAフォーマットと呼ばれるものみたい．  
参照サイト：http://www.hiramine.com/physicalcomputing/general/gps_nmeaformat.html  
研究室内では，GPSが取得できないみたい．  
まあ，これで無事GPSとTheta画像を同時に取得できそうです！  
８８８８８８８８８８８８８８８８８８８８８８８８８  

##５．統合作業  
のこりのタスク  


##６．おまけ  
撮影するたびに「ピョ～ン」と少し耳障りなので，シャッター音を設定できないかと調べたところ以下のサイトが参考になりました．
参照サイト：http://blogs.yahoo.co.jp/honebuto_honebuto/39537206.html  
シータと端末を接続したうえで，  
https://code.google.com/p/scan-manager/downloads/detail?name=gphoto-2.4.14-win32-build2.zip&can=2&q=  
をインストールして，同フォルダ内で以下のコマンドを実行  
gphoto2 --port ptpip:192.168.1.1 --summary  

すると以下のような結果が得られると思います．  
Device Property Summary:  
Battery Level(0x5001):(read only) (type=0x2) Range [0 - 100, step 1] value: 100%  
 (100)
Exposure Bias Compensation(0x5010):(readwrite) (type=0x3) Enumeration [2000,1700  
,1300,1000,700,300,0,-300,-700,-1000,-1300,-1700,-2000] value: 0.0 stops (0)  
Date & Time(0x5011):(readwrite) (type=0xffff) '20130101T000610'  
Property 0x502c:(readwrite) (type=0x6) Range [0 - 100, step 1] value: 50  
Property 0xd006:(read only) (type=0x6) 8  
Property 0xd801:(readwrite) (type=0xffff) ''  
Property 0xd802:(readwrite) (type=0x2) Range [0 - 30, step 1] value: 10  
Property 0xd803:(readwrite) (type=0x4) Range [0 - 1800, step 1] value: 300  
Property 0xd805:(readwrite) (type=0xffff) 'THETAXXXXXX'  
Property 0xd806:(readwrite) (type=0xffff) 'XXXXXXXX'  
Property 0xd807:(readwrite) (type=0x2) Enumeration [0,1,6,11] value: 0  
この中の502cがシャッター音量です。  
デフォルトで50に設定されています。  
Property 0x502c:(readwrite) (type=0x6) Range [0 - 100, step 1] value: 50  

これを0（無音）に変更します。  
gphoto2 --port ptpip:192.168.1.1 --set-config 502c=0  

上手くいくと'event()'と表示されます。  
 
もう一度  
gphoto2 --port ptpip:192.168.1.1 --summary  
を実行して変更されているか確認しましょう。  
 
value: 0になっていれば以上で書き換え終了です。  
他の設定はご自身で、いろいろ試してみてください。  

