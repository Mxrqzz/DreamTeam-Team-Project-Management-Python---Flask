from app.database import create_connection, close_connection
from flask import jsonify
from datetime import datetime


class Team:
    def __init__(self, nome, descricao, criador_id):
        self.nome = nome
        self.descricao = descricao
        self.criador_id = criador_id

    def criar_equipe(self):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()
            try:
                #! Inserindo dados na Tabela equipes
                sql = "INSERT INTO equipes (nome, descricao, criador_id) VALUES (%s, %s, %s)"
                values = (self.nome, self.descricao, self.criador_id)
                cursor.execute(sql, values)
                conexao.commit()

                # *Obter Id da Equipe recem criada
                equipe_id = cursor.lastrowid

                #!Inserir o criador da equipe na tabela equipe_membros

                sql_membro = "INSERT INTO equipe_membros (equipe_id, user_id, cargo) VALUES (%s, %s, %s)"
                values_membro = (equipe_id, self.criador_id, "administrador")
                cursor.execute(sql_membro, values_membro)
                conexao.commit()

                print(f"Equipe {self.nome} cadastrada com sucesso.")

            except Exception as e:
                print(f"Erro ao criar equipe: {e}")
            finally:
                cursor.close()
                close_connection(conexao)
                print("A Conexão com o banco de dados foi encerrada.")


    @staticmethod
    def listar_equipes(user_id):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()

            sql = """
                SELECT 
                    equipes.id, 
                    equipes.nome, 
                    equipes.descricao, 
                    equipes.criado,
                    (SELECT COUNT(*) FROM equipe_membros WHERE equipe_membros.equipe_id = equipes.id) AS qtd_membros,
                    (SELECT COUNT(*) FROM projetos WHERE projetos.equipe_id = equipes.id) AS qtd_projetos,
                    equipe_membros.cargo
                FROM equipes
                JOIN equipe_membros ON equipes.id = equipe_membros.equipe_id
                WHERE equipe_membros.user_id = %s
                GROUP BY equipes.id, equipe_membros.cargo
            """

            try:
                cursor.execute(sql, (user_id,))
                equipes = cursor.fetchall()
                if equipes:
                    return equipes
                else:
                    return None
            except Exception as e:
                print(f"Erro ao listar equipes: {e}")
                return None
            finally:
                close_connection(conexao)



    @staticmethod
    def listar_membros(equipe_id):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()

            sql = """
                SELECT 
                    usuarios.id,
                    usuarios.nome, 
                    usuarios.username, 
                    usuarios.email, 
                    equipe_membros.cargo
                FROM equipe_membros
                JOIN usuarios ON equipe_membros.user_id = usuarios.id
                WHERE equipe_membros.equipe_id = %s
            """

            try:
                cursor.execute(sql, (equipe_id,))
                membros = cursor.fetchall()
                if membros:
                    return membros
                else:
                    return None
            except Exception as e:
                print(f"Erro ao listar membros da equipe: {e}")
                return None
            finally:
                cursor.close()
                close_connection(conexao)

    # Função para alterar o cargo de um membro
    @staticmethod
    def atualizar_cargo(user_id, cargo, equipe_id):
        conexao = create_connection()

        if conexao:
            cursor = conexao.cursor()
            try:
                # Atualiza o cargo do membro na tabela equipe_membros
                sql = "UPDATE equipe_membros SET cargo = %s WHERE user_id = %s AND equipe_id = %s"
                values = (cargo, user_id, equipe_id)
                cursor.execute(sql, values)
                conexao.commit()

                print(f"Cargo do membro com ID {user_id} alterado para {cargo}.")
                return True  # Indica sucesso

            except Exception as e:
                print(f"Erro ao alterar o cargo: {e}")
                return False  # Indica falha
            finally:
                cursor.close()
                close_connection(conexao)

    # Função para adicionar mensagem

    @staticmethod
    def adicionar_mensagem(user_id, equipe_id, mensagem):
        try:
            # Conexão com o banco de dados
            conexao = create_connection()
            cursor = conexao.cursor()

            # Comando SQL para inserir a mensagem
            sql = """
                INSERT INTO mensagens (user_id, equipe_id, mensagem, enviado_em)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(sql, (user_id, equipe_id, mensagem))

            # Commit para salvar a mensagem no banco
            conexao.commit()

            print(f"Mensagem enviada para o time {equipe_id} pelo usuário {user_id}.")
            return True  # Sucesso

        except Exception as e:
            print(f"Erro ao adicionar mensagem: {e}")
            return False  # Falha

        finally:
            # Fechar cursor e conexão
            if cursor:
                cursor.close()
            if conexao:
                close_connection(conexao)

    @staticmethod
    def listar_mensagens(equipe_id):
        mensagens = None
        try:
            conexao = create_connection()
            if conexao:
                cursor = conexao.cursor()
                sql = """
                    SELECT mensagens.*, usuarios.nome 
                    FROM mensagens 
                    JOIN usuarios ON mensagens.user_id = usuarios.id 
                    WHERE mensagens.equipe_id = %s
                    ORDER BY enviado_em ASC
                """  # Remover a vírgula após a string
                cursor.execute(sql, (equipe_id,))
                mensagens = cursor.fetchall()
                

                if mensagens:
                    print("mensagens carregadas")
                    return mensagens
        except Exception as e:
            print(f"Error ao listar mensagens {e}")
        finally:
            close_connection(conexao)

