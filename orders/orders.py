import json
from flask import jsonify, request
from classes.order.connection import connection
from classes.order.basic_auth import auth, app
from classes.utils.manipulation import Convert, Validation
from classes.utils.consumer import Consumer
import classes.utils.vars as v
import requests 
import uuid
from kafka import  KafkaProducer

urlc=f"http://{v.app_endpoint}:8080/clients"
urlp=f"http://{v.app_endpoint}:8082/products"

@app.route('/', methods=['GET'])
def root():
    return jsonify({"Status":"API Orders ok, methods alloweds: GET, POST, PUT, DELETE"}), 200

@app.route("/orders", methods=['GET'])
@auth.required
def getOrder():
    try:
        #Realiza a conexão
        connection.connect()
        cur = connection.cursor()

        try:
            #Criação de parametros personalizados para a query
            idon = ''
            clientidon = ''
            productidon = ''
            orderdateon = ''
            where = ''
            args = []
            if request.args.get('id'):
                idon = 'Id = %s'
                where =  ' WHERE '
                args.append(request.args.get('id'))
            if request.args.get('clientid') and not request.args.get('id'):        
                clientidon = 'clientid = %s'
                where = ' WHERE '
                args.append(request.args.get('clientid'))
            if request.args.get('productid') and not request.args.get('id'):
                if where:
                    productidon = ' AND productid = %s '
                else:
                    productidon = 'productid = %s '
                    where = ' WHERE '
                args.append(request.args.get('productid'))
            if request.args.get('orderdate') and not request.args.get('id'):
                if where:
                    orderdateon = ' AND orderdate LIKE %s %s %s'
                else:
                    orderdateon = 'orderdate LIKE %s %s %s'
                    where = ' WHERE '
                args.append('%')
                args.append(request.args.get('orderdate'))
                args.append('%')

             #Executa a query do select
            if where:
                sqlQuery = f"SELECT id, clientid, productid, orderdate, observation FROM orders {where} {idon} {clientidon} {productidon} {orderdateon}"
                cur.execute(sqlQuery,(args))
            else:
                sqlQuery = "SELECT id, clientid, productid, orderdate, observation FROM orders"
                cur.execute(sqlQuery)
            select = cur.fetchall()
            if not select:
                    return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"},), 404

            #Muda o tipo de data
            for i in select:
                i["orderdate"] = f'{i["orderdate"]}'

            #Conexão com outras apis
            if request.args.get("id") or request.args.get("clientid") or request.args.get("productid") and (request.args.get('client') or request.args.get("product")):
                clients = ''
                products = ''
                #Conexão api client
                if request.args.get("client") == "True" or request.args.get("client") == "true":
                    try:
                        if request.args.get("id"):
                            id = select[0]['clientid']
                            req = requests.get(url=urlc, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":id})
                            clients = req.json()
                        elif request.args.get("clientid"):
                            id = request.args.get("clientid")
                            req = requests.get(url=urlc, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":id})
                            clients = req.json()
                        elif request.args.get("productid") and not (request.args.get("id") or request.args.get("clientid")):
                            clients = []
                            idlist = []
                            for i in select:
                                id = i['clientid']
                                if id not in idlist:
                                    idlist.append(id)
                                    req = requests.get(url=urlc, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":id})
                                    clients.append(req.json())
                    except Exception as e:
                        return jsonify({"Error":"Comunicação com a API de clientes falhou"}), 500
                #Conexão com a api Products
                if request.args.get("product") == "True" or request.args.get("product") == "true":
                    try:
                        if request.args.get("productid") or request.args.get("id"):
                            id = select[0]["productid"]
                            req = requests.get(url=urlp, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":id})
                            products = req.json()
                        else:
                            products = []
                            idlist = []
                            for i in select:
                                id = i['productid']
                                if id not in idlist:
                                    idlist.append(id)
                                    req = requests.get(url=urlp, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":id})
                                    products.append(req.json())
                    except Exception as e:
                        return jsonify({"Error":"Comunicação com a API de produtos falhou"}), 500

                if clients and products:
                    return jsonify(select, clients, products), 200
                elif clients:
                    return jsonify(select, clients), 200
                elif products:
                    return jsonify(select, products), 200

            return jsonify(select), 200
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}),400
    except Exception as e:
        return jsonify({"Error" :"{}".format(e)}), 500
    finally:
        connection.close()
        cur.close()

@app.route("/orders", methods=['POST'])
@auth.required
def postOrder():
    try:
        #Realiza a conexão
        connection.connect()
        cur = connection.cursor()

        #Verifica se o JSON com os dados dos produtos foi enviado de maneira correta
        try:
            if request.json:
                #Verifica os campos do json
                try:
                    _json = request.json
                    _observation = _json['observation']
                    _clientid = _json['clientid']
                    _productid = _json['productid']
                    _json['transaction_id'] = str(uuid.uuid4())

                    #Tratamento da data
                    if not Validation.ValDate(_json['orderdate']):
                        return jsonify({"Error" :"Verique se a data informada em 'orderdate' esta formatada de maneira correta"}), 400
                    _orderdate = Validation.ValDate(_json['orderdate'])

                   #Envio para a fila de NEW_ORDER
                    producer = KafkaProducer(bootstrap_servers=[f"{v.kafka_endpoint}:19092", f"{v.kafka_endpoint}:29092", f"{v.kafka_endpoint}:39092"], 
                        value_serializer=lambda v: json.dumps(v).encode("utf-8")
                        )
                    producer.send("NEW_ORDER", _json).get()

                    #Validação
                    result = Consumer.validateOrder(_json['transaction_id'])
                    
                except Exception as e:
                    return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400

                if(not result):
                    return jsonify({"Status" :f"Status não pode ser obtido, contate o administrador do sistema, id da transação: {_json['transaction_id']} "}), 500  
                if("1e" in result):
                    return jsonify({"Status" :"Registro não concluído, cliente inválido"}), 400
                elif("2e" in result):
                    return jsonify({"Status" :"Registro não concluído, produto inválido"}), 400  
                elif("3e" in result):
                    return jsonify({"Status" :"Registro não concluído, cliente e produto inválidos"}), 400  

                #Executa a query sql
                sqlQuery = "INSERT INTO orders (clientid, productid, orderdate, observation) VALUES (%s,%s,%s,%s)"
                cur.execute(sqlQuery,(_clientid, _productid, _orderdate, _observation))
                connection.commit()
                return jsonify({"Status" :"Registro criado com sucesso"}), 201
            else:
                return jsonify({"Error" :"Verifique se um json valido foi enviado"}), 400
        except Exception as e:
            if e.__str__().find('1062'):
                return jsonify({"Error" :"{}".format(e)}), 409
            else:
                return jsonify({"Error" :"{}".format(e)}), 400
    except Exception as e:
        return jsonify({"Error" :"{}".format(e)}), 500
    finally:
        connection.close()
        cur.close()

@app.route("/orders", methods=['PUT'])
@auth.required
def putOrder():
    if request.args.get('id'):
        try:
            #Realiza a conexão
            connection.connect()
            cur = connection.cursor()
           
            try:
                #Verifica se o id passado corresponde a um registro.
                queryVer = "Select * FROM orders WHERE id = %s;"
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchone()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Verifica se o JSON com os dados dos produtos foi enviado de maneira correta
                if request.json:
                    #Verifica os campos do json
                    try:
                        json = request.json
                        _id = json['id']
                        _clientid = json['clientid']
                        _productid = json['productid']
                        _observation = json['observation']
                        #Tratamento da data
                        if not Validation.ValDate(json['orderdate']):
                            return jsonify({"Error" :"Verique se a data informada em 'orderdate' esta formatada de maneira correta"}), 400
                        _orderdate = Validation.ValDate(json['orderdate'])

                        #Validação de id pela api clients
                        try:
                            req = requests.get(url=urlc, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":_clientid})
                        except Exception as e:
                            return jsonify({"Error":"Comunicação com a API de clientes falhou"}), 500
                        if not req.status_code == 200:
                            return jsonify({"Error" :"O id passado nao corresponde a nenhum cliente"}), 400

                        #Validação de id pela api Products
                        try:
                            req = requests.get(url=urlp, headers={'Authorization':'Basic YWRtaW46YWRtaW4xMjM='}, params={"id":_productid})
                        except Exception as e:
                            return jsonify({"Error":"Comunicação com a API de products falhou"}), 500
                        if not req.status_code == 200:
                            return jsonify({"Error" :"O id passado nao corresponde a nenhum produto"}), 400

                    except Exception as e:
                        return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400

                    #Executa a query sql
                    sqlQuery = "UPDATE orders SET id = %s, clientid = %s, productid = %s, orderdate = %s, observation = %s WHERE id = %s"
                    cur.execute(sqlQuery,(_id,_clientid, _productid, _orderdate, _observation, request.args.get('id')))
                    connection.commit()
                    return jsonify({"Status" :"Registro alterado com sucesso"}), 200
                else:
                    return jsonify({"Error" :"Verifique se um json valido foi enviado"}), 400
            except Exception as e:
                if e.__str__().find('1062'):
                    return jsonify({"Error" :"{}".format(e)}), 409
                else:
                    return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()
    else:
        return jsonify({"Error" :"Verifique o parametro ID"}), 400

@app.route("/orders", methods=['DELETE'])
@auth.required
def deleteOrder():
    if request.args.get('id'):
        try:
            connection.connect()
            cur = connection.cursor()
            try:
                #Verifica se o id passado corresponde a um registro
                queryVer = "Select * FROM orders WHERE id = %s;"
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchone()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Deleta o registro do banco de dados.
                sqlQuery = ("DELETE FROM orders WHERE id = %s;")
                cur.execute(sqlQuery,request.args.get('id'))
                connection.commit()
                return jsonify({"Status" :"Registro deletado com sucesso"}), 200  
                
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()
    else:
        return jsonify({"Error" :"Verifique o parametro ID"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8083, host='0.0.0.0')
