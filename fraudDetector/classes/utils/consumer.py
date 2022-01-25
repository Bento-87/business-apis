import requests
import classes.utils.vars as v

urlc=f"http://{v.app_endpoint}:8080/clients"
urlp=f"http://{v.app_endpoint}:8082/products"

class Consumer:

    def order(order):
        error = 0

        #Validação de id pela api clients
        try:
            req = requests.get(url=urlc, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":order["clientid"]})
            if not req.status_code == 200:
                error += 1
        except Exception as e:
            error += 1 # Client Error

        #Validação de id pela api products
        try:
            req = requests.get(url=urlp, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":order["productid"]})
            if not req.status_code == 200:
                error += 2
        except Exception as e:
            error += 2 # Product Error
        
        #Verificação de disponibilidade do produto
        # if req.json()[0]['availability'] == 'No':
        #     return jsonify({"Error":"O produto nao esta disponivel para venda no momento"}),400
                
        order["status"] = f"{error}e"

        return order