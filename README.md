timerwood_server
================

timerwood todo-list pretty-dumb-storage


Сервер для сохранения данных из timerwood-client


API
1. Создание нового таймера
Запрос
URL: /timer/{timer_code}
где timer_code - название (код) таймера, длина = 32 символа, необязательный параметр
метод: POST

данные POST:
data - текстовые данные таймера (например JSON)

Пример: curl http://82.196.2.175:8062/timer/ -d data="{task83=1}"
ответ: 
...
{
  "guest_code": "lRf34DD0f", 
  "master_code": "biGmN39E", 
  "status": true
}
...

2. Чтение таймера
3. Удаление таймера
