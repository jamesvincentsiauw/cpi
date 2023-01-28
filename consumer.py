from adapter.rabbitmq import RabbitConsumer

def main():
    print('consumer running')
    engine = RabbitConsumer(username='fvybkdkm', password='cjk6uSn_I9jpx48pfkZGofiftv2LqlgI', host='campbell-01.lmq.cloudamqp.com', port=5672, vhost='fvybkdkm', queue_name='cpi.updated')
    engine.run()

if __name__ == '__main__':
    main()
