@echo off
IF EXIST "C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.10\sbin" (
    cd C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.10\sbin
) ELSE (
    set /p cd="Enter Your RabbitMQ Server's sbin directory: "
    cd %cd%
)
rabbitmq-server restart