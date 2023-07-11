from flask import Flask, render_template, request, redirect, url_for
import repositorio

app = Flask(__name__)

@app.route('/')
def home():
    listProducts = repositorio.list_products()
    return render_template("index.html", products=listProducts)

@app.route('/produto/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    if request.method == 'POST':
        #quer dizer que o usuário está mandando dados
        if "excluir" in request.form:
            repositorio.delete_product(id)
            return redirect(url_for('home'))
        elif "salvar" in request.form:
            id = request.form['id']
            nome = request.form['nome']
            preco = request.form['preco']
            promocao = request.form['promocao']
            descricao = request.form['descricao']
            imagem = request.form['imagem']

            dados_retornados = repositorio.get_product(id)
            if dados_retornados:
                repositorio.update_product(id=id, nome=nome , preco=preco, promocao=promocao, descricao=descricao, imagem=imagem)
            else:
                repositorio.create_product(nome=nome , preco=preco, promocao=promocao, descricao=descricao, imagem=imagem)

            return redirect(url_for('home'))
    else:
        id, nome, preco, promocao, descricao, imagem = repositorio.get_product(id)
        return render_template("cadastro.html", id=id, nome=nome , preco=preco, promocao=promocao, descricao=descricao, imagem=imagem)

#HOME PAGE DA LOJA
@app.route('/geekstore', methods=["GET", "POST"])
def home_loja():
    listProducts = repositorio.list_products()
    return render_template("home_loja.html", products=listProducts)

#PRODUTO INDIVIDUAL
@app.route('/geekstore/produto/<int:id>', methods=["GET", "POST"])
def produto_loja(id):
    id, nome, preco, promocao, descricao, imagem = repositorio.get_product(id)
    return render_template("produto_loja.html", id=id, nome=nome , preco=preco, promocao=promocao, descricao=descricao, imagem=imagem)

#CARRINHO DE COMPRAS
@app.route('/geekstore/carrinho', methods=["POST"])
def adicionar_excluir_carrinho():
    if "excluir" in request.form:
        id = request.form['id']
        repositorio.excluir_do_carrinho(id=id)
        return redirect('carrinho')
    elif "finalizar" in request.form:
        ids = str(repositorio.exibir_produtos_carrinho()[0])
        total = float(repositorio.exibir_produtos_carrinho()[1])
        repositorio.finalizar_compra(ids=ids, total=total)
        return render_template("compra_finalizada.html")
    else:
        id = request.form['id']
        nome = request.form['nome']
        preco = request.form['preco']
        promocao = request.form['promocao']
        descricao = request.form['descricao']
        imagem = request.form['imagem']
        repositorio.adicionar_ao_carrinho(id=id, nome=nome, promocao=promocao)
        return redirect('carrinho')
    #return render_template("carrinho.html", id=id, nome=nome , preco=preco, promocao=promocao, descricao=descricao, imagem=imagem)

@app.route('/geekstore/carrinho', methods=["GET"])
def exibir_carrinho():
    listProducts = repositorio.exibir_produtos_carrinho()
    if listProducts:
        total = "{:.2f}".format(listProducts[1])
        return render_template("carrinho.html", products=listProducts[0], total=total)
    else:
        # listProducts = [{"Código": "", "Nome": "", "Preço": ""}]
        # total = 0
        return render_template("carrinho_vazio.html")
    
@app.route('/geekstore/comprafinalizada', methods=['GET'])
def compra_finalizada():
    return render_template("compra_finalizada.html")

app.run(debug=True)