# Base image
FROM rabbitmq:latest

# Enable RabbitMQ management plugin
RUN rabbitmq-plugins enable rabbitmq_management

# Expose necessary ports
EXPOSE 5672 15672

# Copy custom configuration file
COPY ./rabbitmq.conf /etc/rabbitmq/conf.d
COPY ./definitions.json /etc/rabbitmq/

# Define entrypoint
CMD ["rabbitmq-server"]
