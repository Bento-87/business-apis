from flask import jsonify, request
from classes.products.connection import connection
from classes.products.basic_auth import auth, app
from classes.utils.manipulation import Convert, Validation

@app.route('/', methods=['GET'])
def root():
    return jsonify({"Status":"API Products ok, methods alloweds: GET, POST, PUT, DELETE, PATCH"}), 200

@app.route("/products", methods=['GET'])
@auth.required
def getProducts():
    try:
        #Realiza a conexão
        connection.connect()
        cur = connection.cursor()

        try:
            #Criação de parametros personalizados para a query
            idon = ''
            nameon = ''
            priceon = ''
            availabilityon = ''
            where = ''
            args = []
            if request.args.get('id'):
                idon = 'Id = %s'
                where =  ' WHERE '
                args.append(request.args.get('id'))
            if request.args.get('name') and not request.args.get('id'):        
                nameon = 'name LIKE %s %s %s'
                where = ' WHERE '
                args.append('%')
                args.append(request.args.get('name'))
                args.append('%')
            if request.args.get('price') and not request.args.get('id'):
                if where:
                    priceon = ' AND price like %s %s %s '
                else:
                    priceon = 'price LIKE %s %s %s '
                    where = ' WHERE '
                args.append('%')
                args.append(request.args.get('price'))
                args.append('%')
            if request.args.get('availability') and not request.args.get('id'):
                if where:
                    availabilityon = ' AND availability = %s'
                else:
                    availabilityon = 'availability = %s'
                    where = ' WHERE '
                args.append(request.args.get('availability'))

            #Executa a query do select
            if where:
                sqlQuery = f"SELECT id, name, description, price, availability, endoflife from products {where} {idon} {nameon} {priceon} {availabilityon}"
                cur.execute(sqlQuery,(args))
            else:
                sqlQuery = "SELECT id, name, description, price, availability, endoflife from products"
                cur.execute(sqlQuery)
            select = cur.fetchall()
            if not select:
                return jsonify({"Error":"Registro nao encontrado, verifique o(s) parametro(s) passado(s)"}), 404
            return jsonify(select)
        except Exception as e:
            return jsonify({"Error" :"{}".format(e)}), 400
    except Exception as e:
        return jsonify({"Error" :"{}".format(e)}), 500
    finally:
        connection.close()
        cur.close()

@app.route("/products", methods=['POST'])
@auth.required
def postProducts():
    try:
        #Realiza a conexão
        connection.connect()
        cur = connection.cursor()

        #Verifica se o JSON com os dados dos produtos foi enviado de maneira correta
        try:
            if request.json:
                #Verifica os campos do json
                try:
                    json = request.json
                    _id = json['id']
                    _name = json['name']
                    _description = json['description']
                    _price = json['price']
                    _availability = json['availability']
                    #Tratamento da data
                    if not Validation.ValDate(json['endoflife']) and json['endoflife']:
                        return jsonify({"Error" :"Verique se a data informada em 'orderdate' esta formatada de maneira correta"}), 400
                    _endoflife = Validation.ValDate(json['endoflife'])
                except Exception as e:
                    return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400

                #Executa a query sql
                sqlQuery = "INSERT INTO products (Id, Name, Description, Price, Availability, EndOfLife) VALUES (%s,%s,%s,%s,%s,%s)"
                cur.execute(sqlQuery,(_id,_name,_description,_price,_availability,_endoflife))
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

@app.route("/products", methods=['PUT'])
@auth.required
def putProducts():
    if request.args.get('id'):
        try:
            #Realiza a conexão
            connection.connect()
            cur = connection.cursor()
           
            try:
                #Verifica se o id passado corresponde a um registro.
                queryVer = "Select * FROM products WHERE id = %s;"
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
                        _name = json['name']
                        _description = json['description']
                        _price = json['price']
                        _availability = json['availability']
                        #Tratamento da data
                        if not Validation.ValDate(json['endoflife']) and json['endoflife']:
                            return jsonify({"Error" :"Verique se a data informada em 'orderdate' esta formatada de maneira correta"}), 400
                        _endoflife = Validation.ValDate(json['endoflife'])
                    except Exception as e:
                        return jsonify({"Error" :"Json enviado de maneira incorreta, verifique o campo {}".format(e)}), 400

                    #Executa a query sql
                    sqlQuery = "UPDATE products SET Id = %s, Name = %s, Description = %s, Price = %s, Availability = %s, EndOfLife = %s WHERE Id = %s"
                    cur.execute(sqlQuery,(_id,_name,_description,_price,_availability,_endoflife, request.args.get('id')))
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

@app.route("/products", methods=['PATCH'])
@auth.required
def patchProducts():
    if request.args.get('id'):
        try:
            #Realiza a conexão
            connection.connect()
            cur = connection.cursor()
            
            try:
                #Verifica se o id passado corresponde a um registro
                queryVer = "Select * FROM products WHERE id = %s;"
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchone()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Dicionario para verificar quais campos foram enviados
                dict_args = {"name":False,"id":False,"price":False,"availability":False,"endoflife":False,"description":False}
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
                
                  #Cria automaticamente a query do sql
                    sqlQuery = ("UPDATE products SET ")
                    for i in dict_args:
                        if dict_args[i] == True:
                            sqlQuery += "{} = %s, ".format(i)
                            #Tratamento da data
                            if i == "endoflife":
                                if not Validation.ValDate(request.json['endoflife']) and request.json['endoflife']:
                                    return jsonify({"Error" :"Verique se a data informada em 'orderdate' esta formatada de maneira correta"}), 400
                                args_true.append(Validation.ValDate(request.json['endoflife']))   
                            else:     
                                args_true.append(request.json[i])
            
                    #Remove alguns caracteres da query 
                    sqlQuery = sqlQuery[:-2]

                    #adiciona a clausula WHERE ao select
                    sqlQuery += " WHERE id = %s;"
                   
                    #Executa a query Sql
                    args_true.append(request.args.get('id'))
                    cur.execute(sqlQuery,(args_true))
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
    

@app.route("/products", methods=['DELETE'])
@auth.required
def deleteProducts():
    if request.args.get('id'):
        try:
            connection.connect()
            cur = connection.cursor()
            try:
                #Verifica se o id passado corresponde a um registro
                queryVer = "Select * FROM products WHERE id = %s;"
                cur.execute(queryVer, request.args.get('id'))
                select = cur.fetchone()
                if not select:
                    return jsonify({"Error" :"O ID digitado não corresponde a nenhum registro"}), 404

                #Deleta o registro do banco de dados.
                sqlQuery = ("DELETE FROM products WHERE id = %s;")
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
    app.run(debug=True, port=8082, host='0.0.0.0')