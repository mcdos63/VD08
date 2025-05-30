from flask import Flask, render_template, request
import requests

sites = [{'url': 'https://api.api-ninjas.com/v1/trivia',
          'key': '0gkpK19+87kCjvSsHceFpw==0PyKL8grN2zVvr7m'},
         {'url': 'https://zenquotes.io/api/random',
          'key': ''},
         {'url': 'https://quoteslate.vercel.app/api/quotes/random',
          'key': ''}]
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    selected_value = "0"  # Значение по умолчанию
    if request.method == 'POST':
        # Получаем выбранное значение из формы
        selected_value = request.form.get('options', "0")
    st = int(selected_value)
    # Делаем запрос к API
    try:
        resp = requests.get(sites[st]['url'], headers={'X-Api-Key': sites[st]['key']})
        print(st, '|', resp.json())
        data = resp.json()
        if not data:
            return "API не вернул данных"

        res = data[0]
        match st:
            case 0:
                question = res['question']
                answer = res['answer']
            case 1:
                question = res['q']
                answer = res['a']
            case 2:
                question = res['quote']
                answer = res['author']

    except Exception as e:
        return f"Ошибка при запросе к API: {resp.status_code} - {e}"

    return render_template('index.html', question=question, answer=answer, selected_text=sites[st]['url'])

if __name__ == "__main__":
    app.run(debug=True)
