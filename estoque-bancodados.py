
import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    try:
        conn = psycopg2.connect(
            host = os.getenv("host"),
            database = "postgres",
            user = os.getenv("usuario"),
            port = os.getenv("port"),
            password = os.getenv("senha_banco")

        )
        return conn
    except Exception as e:
        print(f'Erro ao conectar no banco de dados:{e}')



def listar_produtos():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SET search_path TO estoque, public;")
        cursor.execute("SELECT * FROM produtos;")
        produtos = cursor.fetchall()
        for p in produtos:
             print(f'ID: {p[0]} | Nome: {p[1]} | Quantidade em estoque: {p[2]} | Valor unitario: {p[3]} |Dt.cadastro: {p[4]}')
    except Exception as e:
        print(f'Não foi possivel listar os produtos: {e}')
    finally:
        conn.commit()
        conn.close()
        cursor.close()


def cadastrar_produto():
    nome = str(input('Digite o nome do produto: '))
    quantidade = int(input('Digite o quantidade: '))
    preco = float(input('Digite o valor unitário do produto: '))
    data_cadastro = datetime.datetime.now()

    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        comando_sql = """INSERT INTO produtos (nome, quantidade_estoque, preco_un, data_cadastro) VALUES (%s, %s, %s,%s) """
        valores = (nome,quantidade,preco,data_cadastro)
        cursor.execute("SET search_path TO estoque, public;")
        cursor.execute(comando_sql, (valores))
        conn.commit()
        print(f'Produto cadastrado com sucesso!')

    except Exception as e:
        print(f'Erro ao cadastrar produto:{e}')
    finally:
        conn.close()
        cursor.close()


def remover_produto():
    nome = input('Digite o nome do produto que deseja retirar do estoque: ')
    nome = nome.strip()
    try:
        conn = conectar_banco()
        cursor = conn.cursor()


        cursor.execute("SET search_path TO estoque, public;")
        cursor.execute("SELECT id, nome, quantidade_estoque, preco_un, data_cadastro FROM produtos WHERE nome ILIKE %s", (f"%{nome}%",))

        produto_encontrado = cursor.fetchall()

        if not produto_encontrado:
            print('Nenhum produto encontrado com essa descrição.')
            return
        else:
            print('Encontrados: \n')
            for p in produto_encontrado:
                print(f'ID: {p[0]} | Nome: {p[1]} | Quantidade: {p[2]} | Vlr.Unit: {p[3]} | Dt.cadastro: {p[4]}')
                 
        encontrados = None

        try:
            id_desejado = int(input('Agora digite o ID do produto que deseja remover do estoque: '))
            for p in produto_encontrado:
                if p[0]== id_desejado:
                    encontrados = p
                    break
        except Exception:
            print('Digite apenas o numero do ID')
            return

        if encontrados:
            id_prod,nome,quantidade,valor,data = encontrados
            print(f'Produto selecionado: {nome}')
            cursor.execute("DELETE FROM produtos WHERE id = %s",(id_prod,))
            print(f'Produto removido com sucesso!')
            conn.commit()
        else:
            print('O ID nao esta entre os listados.')
            

    except Exception as e:
        print(f'Erro ao remover produto: {e}')
    finally:
        if conn:
            conn.close()
            cursor.close()


def buscar_produto():
   
    nome = str(input('Digite o nome do produto: '))
    nome = nome.strip()
    nome = nome.lower()
    valor_coringa = f"%{nome}%"
 
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        comando_sql = """SELECT * FROM produtos WHERE nome ILIKE %s """
        cursor.execute("SET search_path TO estoque, public;")
        cursor.execute(comando_sql,(valor_coringa,))
        p_encontrado =  cursor.fetchall()

        if p_encontrado:
            print(f'Registros encontrados para: {valor_coringa}\n')
            for p in p_encontrado:
                print(f'ID: {p[0]} | Nome: {p[1]} | Quantidade em estoque: {p[2]} | Valor unitario: {p[3]} |Dt.cadastro: {p[4]}')
                conn.commit()
        else:
            print(f'Nenhum valor encontrado para {valor_coringa}')

    except Exception as e:
        print(f'Erro ao buscar produto: {e}')
    finally:
        if conn:
            conn.close()
            cursor.close()



def registrar_saida():
    nome= str(input('Digite o nome do produto para dar saida: \n'))
    nome = nome.strip()
    nome = nome.lower()
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SET search_path TO estoque, public;")
        cursor.execute("SELECT id, nome, quantidade_estoque FROM produtos WHERE nome ILIKE %s", (f"%{nome}%",))
        produtos = cursor.fetchall()
        if not produtos:
            print(f"{nome} não localizado na base de dados")
            return print('Produtos encontrados com essa descrição:\n')
        for p in produtos:
            print(f'ID: {p[0]}| Nome: {p[1]}| Quantidade: {p[2]}')

        try:
            id_selecionado = int(input('Digite o ID do produto desejado: '))
            for p in produtos:
                p[0]== id_selecionado
                encontrados = p
                break
            print(encontrados)
            
        except ValueError:
            print('Digite apenas o ID do produto.')

        if not encontrados:
            print('O ID nao esta entre os listados!')
            return 
        id_produto, nome, quantidade_estoque = encontrados

        try: 
             qtde_saida = int(input('Digite a quantidade de saida: '))

        except ValueError:
            print('Deve ser um numero inteiro!')
            return conn 
        if qtde_saida > quantidade_estoque:
            print(f'Quantidade indisponivel, voce tem apenas isso disponivel: {quantidade_estoque}')
        else:
            nova_qtde = quantidade_estoque - qtde_saida
            cursor.execute("UPDATE produtos SET quantidade_estoque = %s WHERE id = %s", (nova_qtde,id_produto))
            conn.commit()
            print(f'Saida registrada com sucesso! Quantidade atual disponivel:{nova_qtde}')
    except Exception as e:
        print(f'Erro ao registrar saída de estoque: {e}')
    finally:
        conn.close()
        cursor.close()


def verificacao():
    conn = None
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SET search_path to estoque,public;")
        cursor.execute("SELECT * FROM produtos WHERE quantidade_estoque <= 5")

        listagem = cursor.fetchall()

        if not listagem: 
            print('Estoque em dia, nenhum produto em estado critico!')
        else:
            print('Produtos necessitando de reposição:\n'.center(30))
            for p in listagem:
                print(f'ID: {p[0]} | Nome : {p[1]} | QTDE: {p[2]} | Valor: {p[3]} Data: {p[4]}')
            conn.commit()

    except Exception as e:
        print(f'Nao foi possivel listar os produtos: {e}')
    finally: 
        conn.close()
        cursor.close()



def menu_principal():
    print('-'*30)
    print('CONTROLE DE ESTOQUE'.center(30))
    print('-'*30)

    while True:

        print('MENU\n'.center(30))
        print('[1] - VER ESTOQUE')
        print('[2] - CADASTRAR PRODUTO')
        print('[3] - REMOVER PRODUTO')
        print('[4] - BUSCAR PRODUTO')
        print('[5] - REGISTRAR SAIDA')
        print('[6] - SAIR')
        print('[7] - VERIFICAR STATUS')

        opcao = int(input('O que deseja fazer? \n'))
        match opcao:
            case 1:
                listar_produtos()
            case 2:
                cadastrar_produto()
            case 3:
                remover_produto()
            case 4:
                buscar_produto()
            case 5:
                registrar_saida()
            case 6:
                print('Saindo...')
                break
            case 7:
                verificacao()
            case _:
                print('Opção inválida, tente novamente.')

menu_principal()



