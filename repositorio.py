import sqlite3

#Gerar um ID novo
def gerar_id():
    conn = sqlite3.connect('ecommerce_products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='products'")
    next_id = cursor.fetchone()[0]
    return next_id + 1

#Criar um novo produto
def create_product(nome, preco, promocao, descricao, imagem):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO products (nome_product, preco_product, promocao_product, descricao_product, imagem_product) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_insert, (nome, preco, promocao, descricao, imagem))
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id
    except Exception as ex:
        print(ex)
        return 0

#Listar todos os produtos
def list_products():
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_select_todos = "SELECT * FROM products"
        cursor.execute(sql_select_todos)
        products = cursor.fetchall()
        conn.close()
        return products
    except:
        return False

#Mostrar um único produto
def get_product(id:int):
    try:
        print(id)
        if id == 0:
            return gerar_id(), "", "", "", "", ""
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_select_unico = "SELECT * FROM products WHERE id_product = ?"
        cursor.execute(sql_select_unico, (id, ))
        id, nome, preco, promocao, descricao, imagem = cursor.fetchone()
        conn.close()
        return id, nome, preco, promocao, descricao, imagem
    except:
        return False

#Atualizar produto
def update_product(id:int, nome, preco, promocao, descricao, imagem):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_update = "UPDATE products SET nome_product = ?, preco_product = ?, promocao_product = ?, descricao_product = ?, imagem_product = ?  WHERE id_product = ?"
        cursor.execute(sql_update, (nome, preco, promocao, descricao, imagem, id))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False

#Deletar produto
def delete_product(id):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_delete = "DELETE from products WHERE id_product = ?"
        cursor.execute(sql_delete, (id, ))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False

# ---- Carrinho Loja

#Adicionar ao carrinho
def adicionar_ao_carrinho(id, nome, promocao):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO carrinho (id_produto, nome_produto, preco_produto) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (id, nome, promocao))
        id_venda = cursor.lastrowid
        conn.commit()
        conn.close()
        return id_venda
    except Exception as ex:
        print(ex)
        return 0
    
#Exibir produtos do carrinho
def exibir_produtos_carrinho():
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_select_todos = "SELECT * FROM carrinho"
        cursor.execute(sql_select_todos)
        products = cursor.fetchall()
        sql_sum_carrinho = "SELECT SUM(preco_produto) FROM carrinho"
        cursor.execute(sql_sum_carrinho)
        sum_carrinho = round(cursor.fetchone()[0], 2)
        conn.close()
        return (products, sum_carrinho)
    except:
        return False
#Excluir um produto do carrinho
def excluir_do_carrinho(id):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_delete_item = "DELETE FROM carrinho WHERE id_produto=?"
        cursor.execute(sql_delete_item, (id, ))
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return False
    
#Finalizar compra
def finalizar_compra(ids, total):
    try:
        conn = sqlite3.connect('ecommerce_products.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO vendas (id_produtos_vendidos, valor_total) VALUES (?, ?)"
        cursor.execute(sql_insert, (ids, total))
        product_id = cursor.lastrowid
        sql_delete_carrinho = "DELETE FROM carrinho"
        cursor.execute(sql_delete_carrinho)
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        print(ex)
        return 0
