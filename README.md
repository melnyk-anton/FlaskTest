# FlaskTest
Програма працює на localhost (адреса в браузері - http://127.0.0.1:5000)

Список доступних url, з якими працює наша програма:

/api/register (для реєстрації студентів)

/api/delete (для видалення студентів за їх ID)

/api/excel (для реєстрації студентів, дані яких знаходяться в Excel файлі певного шаблону)

/api/change/int:id (для редагування даних студента, id - його ID в Базі Даних)

/api/student/all (поверне дані всіх студентів, які зареєстровані, у файлі json. Також можливе сортування за допомогою додання ключів sorting (можливі значення: 'asc' і 'desc', які відповідно означають у порядку зростання, у порядку спадання) і filter (фільтр за роком народження студента, значення має бути типу int))

/api/student/int:id (поверне дані про студента у файлі json за його id в БД)
   
Також, якщо ввести неправильну url адресу, висвітиться вікно з помилкою, де буде відображений список доступних url