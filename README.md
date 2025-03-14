本程序将administrative_village_layer.shp中空间文件导入到PG库中的空间表

安装
打开项目的虚拟运行环境,相关模块已经手动安装成功

使用方法
配置conf目录下globe.common.conf中的PG配置参数

PG数据库信息
PG_IP = 10.219.23.76
PG_PORT = 20021
PG_USER = postgres
PG_PASSWD = r00t
PG_DB = og4_hb
执行主程序
python shrpfile_load_pg.py
验证结果
SELECT COUNT(*) from administrative_village_layer;
