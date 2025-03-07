from osgeo import ogr, osr
import psycopg2
from sqlalchemy import create_engine, text

# 获取数据库信息

from conf import PushCONF

pg_ip = str(PushCONF().pg_ip)
port = PushCONF().pg_port
user = str(PushCONF().pg_user)
passwd = str(PushCONF().pg_passwd)
pg_db = str(PushCONF().pg_db)
tns = ip + ':' + str(port) + '/' + sid


# 连接PostgreSQL数据库
conn = psycopg2.connect(
    host=pg_ip,
    port=port,  # 通常为5432
    dbname=pg_db,
    user=user ,
    password=passwd
)


def get_engine():
    #connection_string ='postgresql+psycopg2://postgres:r00t@10.219.23.76:20021/og4_hb'
    connection_string = 'postgresql+psycopg2://postgres:iCAN%402024@0.219.200.126:8432/postgres'
    engine = create_engine(connection_string)
    return engine

def create_tb(engine, layer, schema_name, table_name):
    schema_name = schema_name
    table_name = table_name
    # 创建表SQL语句
    create_table_sql = f"""CREATE TABLE {schema_name}.{table_name} (
        """
    # 读取Shapefile中的字段
    for i, field in enumerate(layer.schema):
        # 获取字段名称和类型
        field_name = field.GetName()
        field_type = field.GetType()
        field_type_str = ogr.GetFieldTypeName(field_type)
        # 根据字段类型设置SQL字段类型
        if field_type_str == 'Integer64':
            column_type = 'int'
        elif field_type_str == 'Real':
            column_type = 'FLOAT'
        elif field_type_str == 'String':
            column_type = 'VARCHAR(500)'
        else:
            column_type = 'VARCHAR(200)'  # 默认为文本类型

        # 添加字段到表创建SQL语句
        if i > 0:
            create_table_sql += ", "
        create_table_sql += f"""{field_name} {column_type}"""

    # 添加几何列
    create_table_sql += f"""
        , geom geometry(Geometry, 4326)
    );"""

    # 创建表
    engine.execute(create_table_sql)
    conn.commit()

def load_tb(engine, layer,schema_name, table_name):
    schema_name = schema_name
    table_name = table_name
    # 创建源和目标空间参考系统
    source_srs = osr.SpatialReference()
    target_srs = osr.SpatialReference()

    # 假设源 SRID 是 4326（WGS84），目标 SRID 也是 4326
    source_srs.ImportFromEPSG(4326)
    target_srs.ImportFromEPSG(4326)

    # 创建坐标转换对象
    coord_transform = osr.CoordinateTransformation(source_srs, target_srs)
    # 遍历Shapefile中的所有要素
    for feature in layer:
        # 获取属性值
        attrs = feature.items()

        # 获取几何数据
        geom = feature.GetGeometryRef()
        geom = feature.GetGeometryRef()
        # 转换几何数据
        geom.Transform(coord_transform)
        geom_wkt = geom.ExportToWkt()

        # 构建插入SQL语句
        insert_sql = f"""INSERT INTO {schema_name}.{table_name} ("""
        geom_placeholder = "ST_GeomFromText('%s', 4326)"
        value_placeholders = ', '.join(['%s'] * len(attrs))
        insert_sql += f"""{', '.join(attrs.keys())}) VALUES ({value_placeholders});"""
        #print(insert_sql)
        #print(list(attrs.values()))
        obj_id = list(attrs.values())[1]
        # 执行插入SQL语句
        engine.execute(insert_sql, list(attrs.values()))
        try:
            # 尝试执行一些可能会抛出异常的代码
            engine.execute(
            f"""UPDATE "{schema_name}"."{table_name}"  SET "geom" = ST_GeomFromText(%s, 4326)::geometry(Polygon, 4326) WHERE OBJECTID= %s""",
                (geom.ExportToWkt(), obj_id))
            conn.commit()
        except :
            # 回滚事务
            conn.commit()

            # 处理异常，或者简单地打印异常信息
            print(f"Geometry type (MultiPolygon) does not match column type (Polygon)")
            print(obj_id)
            continue  # 跳过当前迭代，继续下一次循环

        #engine.execute(f"""UPDATE "{schema_name}"."{table_name}"  SET "geom" = ST_GeomFromText(%s, 4326)::geometry(Polygon, 4326) WHERE OBJECTID= %s""",(geom.ExportToWkt(), obj_id))
        conn.commit()

if __name__ == "__main__":
    # 连接PostgreSQL数据库

    conn = psycopg2.connect(
        host=pg_ip,
        port=port,  # 通常为5432
        dbname=pg_db,
        user=user,
        password=passwd
    )

    # 创建一个新的PostgreSQL游标
    engine = conn.cursor()

    # 加载Shapefile
    shapefile_path = 'administrative_village_layer.shp'
    ds = ogr.Open(shapefile_path)
    layer = ds.GetLayer()

    # 设置PostGIS的schema
    schema_name = 'public'
    table_name = 'administrative_village_layer'

    # 建表
    create_tb(engine, layer, schema_name, table_name)

    #加载数据
    load_tb(engine, layer, schema_name, table_name)

    # 关闭游标和连接
    engine.close()
    conn.close()







