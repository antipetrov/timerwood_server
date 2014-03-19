timerwood_server
================

Сервер для сохранения данных из timerwood-client

Сервер понимает REST, то есть запросы надо отправлять по HTTP методами GET,POST,PUT,DELETE
Ответы-всегда в JSON

# Методы API

## 1. Создание нового таймера

**Запрос:**  
**URL**: /timer/{timer_code}/  
где timer_code - название (код) таймера, длина = 32 символа, необязательный параметр  
**метод**: POST  
**данные POST**:  
data - текстовые данные таймера (например JSON), серверу все равно что это будет за текст он его только сохраняет

**Ответ:**  
**status**: true/false (создан/не создан)  
**master_code**: код для последующего просмотра/редактирования/удаления. Если в запросе был timer_code, то master_code == timer_code  
**guest_code**: код только для просмотра  
**error**: текст ошибки, если status == false. Может отсутствовать

Пример: curl http://82.196.2.175:8062/timer/ -d data="{task83=1}"  
ответ: 
`{  
  "guest_code": "lRf34DD0f",  
  "master_code": "biGmN39E",  
  "status": true  
}`


## 2. Чтение таймера
**Запрос:**  
**URL**: /timer/{timer_code}/  
где timer_code - обязательный параметр, код таймера, полученный при создании   
**метод**: GET  


**Ответ:**  
status: true/false (если без ошибок - true)  
**data**: данные таймера  
**mode**: права доступа. Если **master** - можно все, если **guest** - только читать  
**error**: текст ошибки, если status == false. Может отсутствовать

Пример: curl http://82.196.2.175:8062/timer/100500/  
ответ: 
`{  
  "data": "{task83=1}",   
  "mode": "master",  
  "status": true
}`


## 3. Редактирование таймера
**Запрос:**  
**URL**: /timer/{timer_code}/  
где timer_code - обязательный параметр, код таймера, полученный при создании   
**метод**: PUT  
данные:
**data** - новые данные таймера (перезаписывают старые полностью)  

**Ответ:**  
**status**: true/false (запись успешна - true)  
**error**: текст ошибки, если status == false. Может отсутствовать 

Пример: curl -X "PUT" http://82.196.2.175:8062/timer/100500/  -d data="{task83=2}"  
ответ: 
`{  
  "message":"Timer updated"  
  "status": true
}`

## 4. Удаление таймера
**Запрос:**  
URL: /timer/{timer_code}/  
где _timer_code_ - обязательный параметр, код таймера, полученный при создании   
**метод**: DELETE  

**Ответ:**  
**status**: true/false (удаление успешно - true)  
**error**: текст ошибки, если status == false. Может отсутствовать 

Пример: curl -X "DELETE" http://82.196.2.175:8062/timer/100500/    
ответ:   
`{  
  "message": "Timer 113 deleted",   
  "status": true  
}`


## JSONP  
В любой запрос можно добавить параметр (GET или POST) **callback** - тогда результат запроса будет обернут в значение callback.  
Пример: curl http://82.196.2.175:8062/timer/1144/?callback=someFunc

ответ:   
`someFunc({  
  "message": "Timer 113 deleted",   
  "status": true  
})`
