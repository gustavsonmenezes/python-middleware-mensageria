"""
EXEMPLO 3: VERSÃO SIMPLIFICADA COM REDIS QUEUE (RQ)

Este exemplo usa Redis Queue (RQ), que é MUITO mais simples que RabbitMQ
e é perfeito para aprender os conceitos básicos.

Redis é um banco de dados em memória super rápido que também pode funcionar
como um Message Queue.
"""

from redis import Redis
import json
import time
from datetime import datetime

# ============================================================================
# PARTE 1: PRODUTOR (Envia tarefas para a Fila)
# ============================================================================

def produtor_redis():
    """
    Simula um Produtor usando Redis como Message Queue
    """
    
    print("=" * 60)
    print("PRODUTOR - Enviando tarefas para a Fila Redis")
    print("=" * 60)
    
    # Conectar ao Redis (localhost:6379 é o padrão)
    try:
        redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()  # Testar conexão
        print("✓ Conectado ao Redis!\n")
    except Exception as e:
        print(f"✗ Erro ao conectar ao Redis: {e}")
        print("💡 Instale Redis: brew install redis (macOS) ou apt install redis (Linux)")
        return
    
    # Enviar 5 tarefas para a Fila
    fila_name = 'tarefas:fila'
    
    for i in range(1, 6):
        tarefa = {
            'id': i,
            'descricao': f'Processar pedido #{i}',
            'timestamp': datetime.now().isoformat(),
            'valor': 100 * i
        }
        
       
        redis_client.lpush(fila_name, json.dumps(tarefa))
        
        print(f"✓ Tarefa {i} adicionada: {tarefa['descricao']}")
        time.sleep(0.3)
    
    # Ver quantas tarefas estão na Fila
    tamanho_fila = redis_client.llen(fila_name)
    print(f"\n📊 Total de tarefas na Fila: {tamanho_fila}")
    print("✓ Produtor finalizou!")

# ============================================================================
# PARTE 2: CONSUMIDOR (Processa tarefas da Fila)
# ============================================================================

def consumidor_redis():
    """
    Simula um Consumidor usando Redis como Message Queue
    """
    
    print("\n" + "=" * 60)
    print("CONSUMIDOR - Processando tarefas da Fila Redis")
    print("=" * 60)
    
    # Conectar ao Redis
    try:
        redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()
        print("✓ Conectado ao Redis!\n")
    except Exception as e:
        print(f"✗ Erro ao conectar ao Redis: {e}")
        return
    
    fila_name = 'tarefas:fila'
    contador = 0
    
    print("Aguardando tarefas... (Pressione CTRL+C para sair)\n")
    
    try:
        while True:
            # RPOP remove e retorna o último item da lista (FIFO)
            tarefa_json = redis_client.rpop(fila_name)
            
            if tarefa_json is None:
                # Fila vazia, aguardar um pouco antes de verificar novamente
                print("⏳ Nenhuma tarefa na Fila, aguardando...", end='\r')
                time.sleep(1)
            else:
                # Decodificar a tarefa
                tarefa = json.loads(tarefa_json)
                contador += 1
                
                print(f"\n📦 Tarefa {contador} recebida!")
                print(f"   ID: {tarefa['id']}")
                print(f"   Descrição: {tarefa['descricao']}")
                print(f"   Valor: R$ {tarefa['valor']}")
                print(f"   Timestamp: {tarefa['timestamp']}")
                
                # Simular processamento
                print(f"   ⏳ Processando... (3 segundos)")
                time.sleep(3)
                
                print(f"   ✓ Tarefa concluída!")
                
                # Ver quantas tarefas ainda estão na Fila
                tamanho_fila = redis_client.llen(fila_name)
                print(f"   📊 Tarefas restantes na Fila: {tamanho_fila}\n")
    
    except KeyboardInterrupt:
        print("\n\n✓ Consumidor parado!")

# ============================================================================
# PARTE 3: DEMONSTRAÇÃO COMPLETA
# ============================================================================

def demo_completa():
    """
    Executa a demonstração completa
    """
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  MIDDLEWARE DE MENSAGERIA - EXEMPLO COM REDIS".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Executar Produtor
    produtor_redis()
    
    # Executar Consumidor
    consumidor_redis()

if __name__ == '__main__':
    demo_completa()