from ksql import KSQLAPI
import classes.utils.vars as v

class Consumer:

    def validateOrder(uuid):

        client = KSQLAPI(f'http://{v.ksql_endpoint}:8088')

        result = client.query(f"select status from order_confirmation where transaction_id = '{uuid}';",  use_http2=True)
       
        i=0
        j=0        
        while i < 5:
            for item in result:
                if(item):
                    j +=1
                if(j > 1):
                  return item
            i+=1

        return False