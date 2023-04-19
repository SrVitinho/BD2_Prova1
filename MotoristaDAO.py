from pymongo import MongoClient
from Classes import Passageiro, Corrida, Motorista
from bson.objectid import ObjectId

class MotoristaDAO:
    def __init__(self, database):
        self.db = database

    def crt_motorista(self, motorista):
        try:
            motorista_dict = {
                "Nota_do_motorista" : motorista.nota_motorista,
                "Corridas" : [
                    {
                        "Nota_da_corrida" : corrida.nota_corrida,
                        "Distancia" : corrida.distancia,
                        'valor': corrida.valor,
                        'passageiro': {
                            'nome': corrida.passageiro.nome,
                            'documento': corrida.passageiro.documento
                        }
                    } for corrida in motorista.corridas
                ]
            }
            r = self.db.collection.insert_one(motorista_dict)
            print(f"Motorista cadastrado com: {r.inserted_id}")
            return r.inserted_id
        except Exception as e:
            print(f"Ocorreu um erro ao criar o motorista: {e}")
            return None

    def read_motorista_by_id(self, id: str):
        try:
            motorista_dict = self.db.collection.find_one({"_id": ObjectId(id)})
            if(motorista_dict):
                notas = motorista_dict['Nota_do_motorista']
                corridas_dict = motorista_dict['Corridas']
                corridas = [Corrida(corrida_dict['Nota_da_corrida'], corrida_dict['Distancia'], corrida_dict['valor'], Passageiro(corrida_dict['passageiro']['nome'], corrida_dict['passageiro']['documento'])) for corrida_dict in corridas_dict]
            print(f"Motorista encontrado: {motorista_dict}")
            return Motorista(notas, corridas)
        except Exception as e:
            print(f"Ocorreu um erro ao ler o motorista: {e}")
            return None

    def upd(self, motorista_id, motorista):
        try:
            motorista_dict = {
                'Nota_do_motorista': motorista.nota_motorista,
                'Corridas': [
                    {
                        'Nota_da_corrida': corrida.nota_corrida,
                        'Distancia': corrida.distancia,
                        'valor': corrida.valor,
                        'passageiro': {
                            'nome': corrida.passageiro.nome,
                            'documento': corrida.passageiro.documento
                        }
                    } for corrida in motorista.corridas
                ]
            }
            res = self.db.collection.update_one({"_id": ObjectId(motorista_id)}, {"$set": motorista_dict})
            print(f"Motorista atualizado: {res.modified_count} documento(s) modificado")
            return res.modified_count
        except Exception as e:
            print(f"Ocorreu um erro ao atualizar o motorista: {e}")
            return None

    def del_motorista(self, id: str):
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"Motorista deletado: {res.deleted_count} documento(s) deletados")
            return res.deleted_count
        except Exception as e:
            print(f"Ocorreu um erro ao deletar o motorista: {e}")
            return None