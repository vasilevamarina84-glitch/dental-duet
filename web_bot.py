from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# ============================================
# БАЗА ЗНАНИЙ (такая же, как была)
# ============================================

knowledge_base = {
    "привет": "Здравствуйте! Чем могу помочь?",
    "здравствуйте": "Добрый день! Я виртуальный помощник стоматологии.",
    "цена": "Стоимость зависит от услуги. Например: чистка зубов — от 3000 ₽, лечение кариеса — от 5000 ₽.",
    "стоимость": "Стоимость зависит от услуги. Например: чистка зубов — от 3000 ₽, лечение кариеса — от 5000 ₽.",
    "запись": "Чтобы записаться на приём, напишите 'записаться' и ваше имя.",
    "записаться": "Отлично! Я записал вас. Администратор свяжется с вами.",
    "график": "Мы работаем с 9:00 до 21:00, без выходных.",
    "режим работы": "Мы работаем с 9:00 до 21:00, без выходных.",
    "адрес": "Мы находимся по адресу: ул. Пушкина, д. 10, офис 5.",
    "спасибо": "Пожалуйста! Всегда рада помочь 😊",
    "пока": "До свидания! Будьте здоровы!",
}

def get_answer(user_input):
    user_input = user_input.lower()
    for keyword in knowledge_base:
        if keyword in user_input:
            return knowledge_base[keyword]
    return "Я пока не знаю ответа на этот вопрос."

# ============================================
# HTML-интерфейс (встроенная страница)
# ============================================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Чат-бот стоматология "Дуэт"</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f8ff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 450px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            background: #fafafa;
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 15px;
            max-width: 80%;
        }
        .user {
            background: #3498db;
            color: white;
            align-self: flex-end;
            margin-left: auto;
            text-align: right;
        }
        .bot {
            background: #ecf0f1;
            color: #2c3e50;
            align-self: flex-start;
            margin-right: auto;
        }
        .chat-input {
            display: flex;
            padding: 15px;
            background: white;
            border-top: 1px solid #ddd;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
            font-size: 14px;
        }
        .chat-input button {
            background: #2c3e50;
            color: white;
            border: none;
            padding: 10px 20px;
            margin-left: 10px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
        }
        .chat-input button:hover {
            background: #1a252f;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            🦷 стоматология "Дуэт"
        </div>
        <div class="chat-box" id="chat-box">
            <div class="message bot">Здравствуйте! Я виртуальный помощник стоматологии "Дуэт". Чем могу помочь?</div>
        </div>
        <div class="chat-input">
            <input type="text" id="user-input" placeholder="Напишите сообщение..." />
            <button onclick="sendMessage()">Отправить</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            const chatBox = document.getElementById('chat-box');

            // Добавляем сообщение пользователя
            const userDiv = document.createElement('div');
            userDiv.className = 'message user';
            userDiv.textContent = message;
            chatBox.appendChild(userDiv);

            // Очищаем поле ввода
            input.value = '';

            // Прокручиваем вниз
            chatBox.scrollTop = chatBox.scrollHeight;

            // Отправляем запрос на сервер
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot';
                botDiv.textContent = data.answer;
                chatBox.appendChild(botDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }

        // Отправка по нажатию Enter
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

# ============================================
# МАРШРУТЫ (РОУТЫ) ВЕБ-ПРИЛОЖЕНИЯ
# ============================================

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    answer = get_answer(user_message)
    return jsonify({'answer': answer})

# ============================================
# ЗАПУСК
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)