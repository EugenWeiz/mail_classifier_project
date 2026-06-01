#!/bin/bash

RUN_LOG_FILE="logs/run.log"
mkdir -p "logs"
echo "Запуск проекта классификации писем"

# Запуск Python-приложение и сохранение весь вывод в run.log
PYTHONUTF8=1 python -m src.mail_classifier.main > "$RUN_LOG_FILE" 2>&1
PROGRAM_STATUS=$?

if [ $PROGRAM_STATUS -eq 0 ]; then
    echo "Проект успешно завершил работу"
    echo "Лог запуска сохранён в: $RUN_LOG_FILE"
    exit 0
else
    echo "Во время запуска проекта произошла ошибка"
    echo "Подробности можно посмотреть в: $RUN_LOG_FILE"
    exit $PROGRAM_STATUS
fi
