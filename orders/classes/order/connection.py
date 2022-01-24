import pymysql.cursors
import pymysql
from ..utils import vars as v

 # Conexão com o banco de dados
connection = pymysql.connect(host=v.db_endpoint,
                            user=v.db_user,
                            password=v.db_password,
                            db='_order',
                            cursorclass=pymysql.cursors.DictCursor)
