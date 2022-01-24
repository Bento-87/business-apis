from flask import Flask
from flask import jsonify, flash, request
from classes.address.connection import connection
from classes.address.basic_auth import auth, app

@app.route('/', methods=['GET'])
def root():
    return jsonify({"Status":"API Address ok, methods alloweds: GET, POST, PUT, DELETE"}), 200

@app.route("/addresses", methods=['GET'])
@auth.required
def get_adresses():
    # Trabalha as requisições feitas com o verbo GET
    if request.method == 'GET':
        try:
           #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()
            
            # Filtra o select com base em pârametros passados pelo usuário
            #Filtragem id
            if request.args.get('id') and not request.args.get('zipcode') and not request.args.get('clientid'):
                try:
                    querySql = "SELECT id, number, street, complement, neighborhod, city, state, country, zipcode, clientid FROM address WHERE id = %s ;"
                    cur.execute(querySql, request.args.get('id'))
                    select = cur.fetchone()
                    if select:
                        return jsonify(select)
                    else:
                        return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"}), 404
                except Exception as e:
                    return jsonify({"Error" :"{}".format(e)}), 400

            #Filtragem CEP
            elif request.args.get('zipcode') and not request.args.get('id') and not request.args.get('clientid') :
                try:
                    querySql = "SELECT id, number, street, complement, neighborhod, city, state, country, zipcode, clientid FROM address WHERE zipcode LIKE %s %s %s ;"
                    cur.execute(querySql,('%',request.args.get('zipcode'),'%'))
                    select = cur.fetchall()
                    if select:
                        return jsonify(select)
                    else:
                        return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"}), 404
                except Exception as e:
                    return jsonify({"Error" :"{}".format(e)}), 400

            #Filtragem ID cliente
            elif request.args.get('clientid') and not request.args.get('id') and not request.args.get('zipcode'):
                try:
                    querySql = "SELECT id, number, street, complement, neighborhod, city, state, country, zipcode, clientid FROM address WHERE clientid = %s ;"
                    cur.execute(querySql,(request.args.get('clientid')))
                    select = cur.fetchall()
                    if select:
                        return jsonify(select)
                    else:
                        return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"}), 404
                except Exception as e:
                    return jsonify({"Error" :"{}".format(e)}), 400

            #Sem filtragem
            else:
                try:
                    querySql = "SELECT id, number, street, complement, neighborhod, city, state, country, zipcode, clientid FROM address;"
                    cur.execute(querySql)
                    select = cur.fetchall()
                    return jsonify(select)
                except Exception as e:
                    return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()

@app.route("/addresses", methods=['POST'])
@auth.required
def post_adresses():
      # Trabalha as requisições feitas com o verbo GET
    if request.method == 'POST':
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            #Lista com o nome dos campos do BD.
            args = ['id','number','street','complement','neighborhod','city','state','country','zipcode']
            args_client = {'clientid':False,'clientcpf':False}
            client = ''

            #Lista com os valores dos campos dos campos
            args_val = []
            
            try:
                if request.json:
                    json = request.json
                    #For para verificar os campos relacionados ao endereço
                    for i in args:
                        try: 
                            json[i]
                            args_val.append(json[i])
                        except Exception as e:
                            return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400

                    #For para verificar os campos relacionados ao cliente
                    for i in args_client:
                        try:
                            json[i]
                            args_client[i] = True
                            client = json[i]
                            break
                        except:
                            args_client[i] = False
                    #Verifica o campo clientid ou client cpf
                    if args_client['clientid'] == False and args_client['clientcpf'] == False:
                            return jsonify({"Error" :"Verifique o campo clientcpf ou clientid"}), 400

                    #Criação da query sql
                    querySql = "INSERT INTO address("
                    for i in args:
                        querySql += f'{i}, '
                    querySql += "clientid)"

                    #Values
                    querySql += (" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
 
                    if args_client['clientcpf'] == True:
                        #Procura o id do cliente cujo cpf foi passado
                        query = "SELECT id FROM clients_data WHERE cpf = %s;"
                        cur.execute(query,client)
                        select = str(cur.fetchone())
                        if select == "None":
                             return jsonify({"Error" :"CPF passado nao corresponde a nenhum cliente"}), 404
                        client = select[6:-1]
                     
                    #Execução da Query
                    args_val.append(client)
                    args_tuple = (args_val)
                    cur.execute(querySql,(args_tuple))
                    connection.commit()
                    return jsonify({"Status" :"Registro criado com sucesso"}), 201
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()

@app.route("/addresses", methods=['PUT'])
@auth.required
def put_adresses():
      # Trabalha as requisições feitas com o verbo GET
    if request.method == 'PUT' and request.args.get('id'):
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            try:
                 #Verifica se o id passado corresponde a um registro.
                queryVer = ("SELECT * FROM address WHERE id = %s")
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchall()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404


                #Lista para checagem e recuperação de valores do JSON
                args = ['id','number','street','complement','neighborhod','city','state','country','zipcode','clientid']
                args_val = []
                #Verificação e recuperação dos valores
                if request.json:
                    json = request.json
                    for i in args:  
                        try: 
                            json[i]
                            args_val.append(json[i])
                        except Exception as e:
                            return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400
                
                #Criacção da Query Sql
                args_val.append(request.args.get('id'))
                args_tuple = (args_val)
                sqlQuery = "UPDATE address SET id  = %s, number = %s, street = %s, complement = %s, neighborhod = %s, city = %s, state = %s, country = %s, zipcode = %s, clientid = %s WHERE id = %s ;"
                cur.execute(sqlQuery,args_tuple)
                connection.commit()
                return jsonify({"Status" :"Registro alterado com sucesso"}), 200
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()
    else:
       return jsonify({"Error" :"Verifique o parametro ID"}), 400


@app.route("/addresses", methods=['DELETE'])
@auth.required
def delete_adresses():
      # Trabalha as requisições feitas com o verbo GET
    if request.method == 'DELETE' and request.args.get('id'):
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            try:
                _id = str(request.args.get('id'))
                #Verifica se o ID passado é um número
                if not _id.isnumeric():
                    return jsonify({"Error" :"Verifique o parametro ID"}), 400

                #Verifica se o id passado corresponde a um registro.
                queryVer = ("SELECT * FROM address WHERE id = %s")
                cur.execute(queryVer, _id)
                select = cur.fetchall()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Montar a query sql
                sqlQuery = "DELETE FROM address WHERE id = %s;"
                cur.execute(sqlQuery,_id)
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
    app.run(debug=True, port=8081, host='0.0.0.0')