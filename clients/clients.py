from flask import jsonify, flash, request
from classes.clients.connection import connection
from classes.clients.basic_auth import auth, app

@app.route('/', methods=['GET'])
def root():
    return jsonify({"Status":"API clients ok, methods alloweds: GET, POST, PUT, DELETE"}), 200

@app.route('/clients', methods=['GET'])
@auth.required
def get_clients():
    # Trabalha as requisições feitas com o verbo GET
    if request.method == 'GET':
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            #Criação de parametros personalidos para as querys.
            idon = ''
            nameon = ''
            args = []
            where = ''
            if request.args.get('id'):
                idon = 'clients_data.id = %s'
                where = ' WHERE '
                args.append(request.args.get('id'))
            if request.args.get('name') and not request.args.get('id'):
                nameon = 'name LIKE %s %s %s'
                where = ' WHERE '
                args.append('%')
                args.append(request.args.get('name'))
                args.append('%')

              #Verificação do parametro address
            if request.args.get('address') == "true" and  where:
                add = ", a.id, a.number, a.street   , a.complement, a.neighborhod, a.city, a.state, a.country, a.zipcode"
                join = "INNER JOIN address as a ON a.clientid = clients_data.id"
            elif request.args.get('address') == "only":
                    add = " a.id, a.number, a.street, a.complement, a.neighborhod, a.city, a.state, a.country, a.zipcode"
                    join = "INNER JOIN address as a ON a.clientid = clients_data.id"
            elif request.args.get('address') == "all" and where: 
                add = ", a.id, a.number, a.street, a.complement, a.neighborhod, a.city, a.state, a.country, a.zipcode"
                join = "LEFT JOIN address as a ON a.clientid = clients_data.id"
            else:
                add = ''
                join = ''

            #Execução do select
            try:
                sqlQuery = f"SELECT clients_data.id, name, cpf, email, gender, phone {add} FROM clients_data {join} {where} {idon} {nameon};" 
                if request.args.get('address') == 'only':
                    sqlQuery = f"SELECT {add} FROM clients_data {join} {where} {idon} {nameon}"
                if where:
                    args = (args)
                    cur.execute(sqlQuery, args)
                else:
                    if request.args.get('address') == "only":
                        sqlQuery = f"SELECT {add} FROM clients_data {join}"
                    else:
                        sqlQuery = f"SELECT clients_data.id, name, cpf, email, gender, phone FROM clients_data;"
                    cur.execute(sqlQuery)
                select = cur.fetchall()
                if select:
                    json = jsonify(select)
                    return json
                else:
                    return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"}), 404
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()

@app.route('/clients', methods=['POST'])
@auth.required
def post_clients():
    # Trabalha as requisições feitas com o verbo POST
    if request.method == 'POST':
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            #Verifica se o JSON com os dados dos clientes foi enviado de maneira correta
            try:
                if request.json:
                    #Verificação de campos do json
                    try:
                        json = request.json
                        _id = json['id']
                        name = json['name']
                        cpf = json['cpf']
                        email = json['email']
                        gender = json['gender']
                        phone = json['phone']
                    except Exception as  e:
                        return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400
                    try:
                        #Executa a query sql
                        sqlQuery = ("INSERT INTO clients_data (id,name,cpf,email,gender,phone) VALUES(%s,%s,%s,%s,%s,%s)")
                        cur.execute(sqlQuery,(_id,name,cpf,email,gender,phone))
                        connection.commit()
                        return jsonify({"Status" :"Registro criado com sucesso"}), 201
                    except Exception as e:
                        if e.__str__().find('1062'):
                            return jsonify({"Error" :"{}".format(e)}), 409
                else:
                    return jsonify({"Error" :"Verifique se um json valido foi enviado"}), 400    
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()

@app.route('/clients', methods=['PUT'])
@auth.required
def put_clients():
    if request.method == 'PUT' and request.args.get('id'):
        try:
            #Realiza a conexão 
            connection.connect()
            cur = connection.cursor()

            #Verifica a estrutura do JSON
            try:
                #Verifica se o id passado corresponde a um registro.
                queryVer = ("SELECT * FROM clients_data WHERE id = %s")
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchall()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                if request.json:
                    #Verifica o corpo do JSON
                    try:
                        json = request.json
                        _id = json['id']
                        name = json['name']
                        cpf = json['cpf']
                        email = json['email']
                        gender = json['gender']
                        phone = json['phone']
                    except Exception as e:
                        return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400
                    #Executar uma query SQL
                    sqlQuery = ("UPDATE clients_data SET id = %s, name = %s, cpf = %s, email  = %s, gender = %s, phone = %s WHERE id = %s;")
                    cur.execute(sqlQuery,(_id,name,cpf,email,gender,phone,request.args.get('id')))
                    connection.commit()
                    return jsonify({"Status" :"Registro alterado com sucesso"}), 200
                else:
                    return jsonify({"Error" :"Verifique se um json valido foi enviado"}), 400       
            except Exception as e:
                return jsonify({"Error" :"{}".format(e)}), 400
        except Exception as e:
              return jsonify({"Error" :"{}".format(e)}), 500
        finally:
            connection.close()
            cur.close()
    else:
        return jsonify({"Error" :"Verifique o parametro ID"}), 400

@app.route("/clients", methods=['PATCH'])
@auth.required
def patch_clients():
    if request.method == 'PATCH' and request.args.get('id'):
        try:
            #Realize a conexão
            connection.connect()
            cur = connection.cursor()
            
            try:
                #Verifica se o id passado corresponde a um registro.
                queryVer = ("SELECT * FROM clients_data WHERE id = %s")
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchall()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Dicionario para verificar quais campos foram enviados
                dict_args = {"name":False,"id":False,"cpf":False,"phone":False,"email":False,"gender":False}
                args_true = []

                #Verifica a estrutura do JSON ---------------------------------
                if request.json:
                    #Verifica quais campos do JSON foram enviados 
                    for i in dict_args:
                        try:
                            request.json[i]
                            dict_args[i] = True
                        except:
                            dict_args[i] = False
                else:
                    return jsonify({"Error" :"Json enviado de maneira incorreta"}), 400
                  
                #Cria automaticamente a query do sql
                sqlQuery = ("UPDATE clients_data SET ")
                for i in dict_args:
                    if dict_args[i] == True:
                        sqlQuery += "{} = %s, ".format(i)
                        args_true.append(request.json[i])
        
                #Remove alguns caracteres da query 
                sqlQuery = sqlQuery[:-2]

                #adiciona a clausula WHERE ao select
                sqlQuery += " WHERE id = %s;"

                #Transforma a lista em tupla para a query
                args_true.append(request.args.get('id'))
                args_tuple = tuple(args_true)

                #Executa a query Sql
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

@app.route("/clients", methods=['DELETE'])
@auth.required
def del_client():
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
                queryVer = ("SELECT * FROM clients_data WHERE id = %s")
                cur.execute(queryVer, _id)
                select = cur.fetchall()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Deleta o registro do banco de dados.
                sqlQuery = ("DELETE FROM clients_data WHERE id = %s;")
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
    app.run(debug=True, port=8080, host='0.0.0.0')