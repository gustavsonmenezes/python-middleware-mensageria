#!/usr/bin/env python3
"""
EXEMPLO 2: CONSUMIDOR (Quem processa as mensagens da Fila)

Este script simula um Consumidor que fica escutando a Fila 'tarefas' e
processa as mensagens conforme elas chegam.

Analogia: É como um carteiro que fica verificando a caixa de correio
e entregando as cartas assim que chegam.
"""

import pika
import json
import time

def callback(ch, method, properties, body):
    """
    Esta função é chamada sempre que uma mensagem chega na Fila.
    
    Args:
        ch: Canal de comunicação
        method: Metadados da mensagem (como o ID de entrega)
        properties: Propriedades da mensagem
        body: O conteúdo da mensagem
    """
    
    try:
        # 1. Decodificar a mensagem (ela vem como bytes)
        mensagem = json.loads(body.decode('utf-8'))
        
        print(f"\n📦 Mensagem recebida!")
        print(f"   ID: {mensagem['id']}")
        print(f"   Tarefa: {mensagem['tarefa']}")
        print(f"   Timestamp: {mensagem['timestamp']}")
        print(f"   Dados: {mensagem['dados']}")
        
        # 2. Simular o processamento da mensagem (o trabalho pesado)
        print(f"   ⏳ Processando... (simulando 2 segundos de trabalho)")
        time.sleep(2)
        
        # 3. Se chegou aqui, o processamento foi bem-sucedido
        print(f"   ✓ Tarefa concluída com sucesso!")
        
        # 4. Confirmar ao RabbitMQ que a mensagem foi processada
        # (Isso remove a mensagem da Fila)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"   ✗ Erro ao processar: {e}")
        # Se algo der errado, não confirmar (a mensagem volta para a Fila)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def consumidor():
    """
    Conecta ao RabbitMQ e fica escutando a Fila 'tarefas'
    """
    
    # 1. Conectar ao RabbitMQ
    print("[CONSUMIDOR] Conectando ao RabbitMQ...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # 2. Declarar a Fila (mesma Fila do Produtor)
    print("[CONSUMIDOR] Declarando a Fila 'tarefas'...")
    channel.queue_declare(queue='tarefas', durable=True)
    
    # 3. Configurar o "prefetch" - quantas mensagens o Consumidor pega por vez
    # Neste caso, 1 significa: pega 1 mensagem, processa, depois pega a próxima
    # (Evita que um Consumidor sobrecarregue)
    channel.basic_qos(prefetch_count=1)
    
    # 4. Registrar a função callback que será chamada quando mensagens chegarem
    print("[CONSUMIDOR] Registrando callback para a Fila 'tarefas'...")
    channel.basic_consume(queue='tarefas', on_message_callback=callback)
    
    # 5. Começar a escutar (fica em loop infinito)
    print("[CONSUMIDOR] Aguardando mensagens... (Pressione CTRL+C para sair)\n")
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n[CONSUMIDOR] Parando de escutar...")
        channel.stop_consuming()
        connection.close()
        print("[CONSUMIDOR] Conexão fechada.")

if __name__ == '__main__':
    try:
        consumidor()
    except Exception as e:
        print(f"[ERRO] {e}")
        print("\n💡 Dica: Certifique-se de que o RabbitMQ está rodando!")
        print("   Para instalar e rodar localmente:")
        print("   - Docker: docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3")
        print("   - Ou instale manualmente: https://www.rabbitmq.com/download.html")