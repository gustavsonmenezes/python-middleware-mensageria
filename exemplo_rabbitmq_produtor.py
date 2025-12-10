"""
EXEMPLO 1: PRODUTOR (Quem envia as mensagens para a Fila)

Este script simula um Produtor que envia pedidos de trabalho para uma Fila
no RabbitMQ. O Produtor não espera o resultado, apenas envia e segue.

Analogia: É como você escrever uma carta e depositar na caixa de correio.
Você não fica esperando o carteiro entregar, você segue com sua vida.
"""

import pika
import json
import time
from datetime import datetime

def produtor():
    """
    Conecta ao RabbitMQ e envia mensagens para a Fila chamada 'tarefas'
    """
    
    # 1. Conectar ao RabbitMQ (localhost:5672 é o padrão)
    print("[PRODUTOR] Conectando ao RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # 2. Declarar a Fila (se não existir, cria; se existir, usa a existente)
    print("[PRODUTOR] Declarando a Fila 'tarefas'...")
    channel.queue_declare(queue='tarefas', durable=True)
    
    # 3. Enviar 10 mensagens para a Fila
    print("[PRODUTOR] Iniciando envio de mensagens...\n")
    
    for i in range(1, 11):
        # Criar uma mensagem (pode ser qualquer coisa: JSON, texto, etc)
        mensagem = {
            'id': i,
            'tarefa': f'Processar pedido #{i}',
            'timestamp': datetime.now().isoformat(),
            'dados': f'Dados importantes do pedido {i}'
        }
        
        # Converter para JSON
        corpo_mensagem = json.dumps(mensagem)
        
        # Publicar a mensagem na Fila
        channel.basic_publish(
            exchange='',  # Usar o exchange padrão
            routing_key='tarefas',  # Nome da Fila
            body=corpo_mensagem,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # Persistir a mensagem
            )
        )
        
        print(f"✓ Mensagem {i} enviada: {mensagem['tarefa']}")
        time.sleep(0.5)  # Pequeno delay para simular chegada de pedidos
    
    print(f"\n[PRODUTOR] Todas as {10} mensagens foram enviadas para a Fila!")
    print("[PRODUTOR] O Produtor não espera nada, ele segue com sua vida.")
    
    # 4. Fechar a conexão
    connection.close()
    print("[PRODUTOR] Conexão fechada.")

if __name__ == '__main__':
    try:
        produtor()
    except Exception as e:
        print(f"[ERRO] {e}")
        print("\n💡 Dica: Certifique-se de que o RabbitMQ está rodando!")
        print("   Para instalar e rodar localmente:")
        print("   - Docker: docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3")
        print("   - Ou instale manualmente: https://www.rabbitmq.com/download.html")