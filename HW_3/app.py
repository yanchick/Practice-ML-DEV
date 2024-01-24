from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import os
import secrets
import csv
import collections

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

users = {}

model_name=''

request_history = collections.defaultdict(list)

category_mapping = {}

with open("models/processed_pricerunner_aggregate.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        category_id = int(row['Category_ID'])
        if category_id in category_mapping:
            continue
        category_label = row['Category_Label']
        category_mapping[category_id] = category_label

models = {}
model_names = ["catboost", "log_reg", "naive_bayes"]

for model_name in model_names:
    model_path = os.path.join("models", f"{model_name}.pkl")
    with open(model_path, "rb") as file:
        models[model_name] = pickle.load(file)


tfidf_path = "models/tfidf.pkl"
with open(tfidf_path, "rb") as file:
    tfidf = pickle.load(file)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], balance=users[session['username']]['balance'],request_history=request_history[session['username']])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username is already taken. Please choose another one.', 'error')
            return redirect(url_for('register'))

        if not (len(password) >= 8 and any(c.isalpha() for c in password) and
                any(c.isdigit() for c in password) and any(c.isupper() for c in password)):
            flash('Password must be at least 8 characters long and contain letters, numbers, and uppercase characters.', 'error')
            return redirect(url_for('register'))

        new_user = {'username': username, 'password': password, 'balance': 100}
        users[username] = new_user

        session['username'] = username

        flash('Registration successful. Welcome to the application!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    if 'username' in session:
        if request.method == 'POST':
            input_description = request.form['input_description']
            selected_model = request.form['selected_model']

            loaded_model = models.get(selected_model)


            if loaded_model is not None:
                price,_=get_price(selected_model)
                if users[session['username']]['balance'] < price:
                    error_message = "Insufficient credits. Please recharge your balance."
                    return render_template('dashboard.html',
                                           username=session['username'],
                                           balance=users[session['username']]['balance'],
                                           error=error_message,
                                           request_history=request_history[session['username']])

                input_description_tr = tfidf.transform([input_description])

                prediction = loaded_model.predict(input_description_tr).item()
                predicted_category = category_mapping.get(prediction, 'Other category')

                price, model_name = get_price(selected_model, 0)
                users[session['username']]['balance'] -= price
                request_history[session['username']].append({
                    'username': session['username'],
                    'input_description': input_description,
                    'Model': model_name,
                    'prediction': predicted_category
                })

                return render_template('dashboard.html',
                                       username=session['username'],
                                       balance=users[session['username']]['balance'],
                                       prediction=predicted_category,
                                       selected_model=model_name,
                                       price=price,
                                       request_history=request_history[session['username']])
            else:
                return render_template('dashboard.html',
                                       username=session['username'],
                                       balance=users[session['username']]['balance'],
                                       error=f"Model {model_name} not found",
                                       request_history=request_history[session['username']])
    return redirect(url_for('login'))

def get_price(model, name=None):
    if model == "log_reg":
        if name:
            return 5, "Logistic Regression"
        return 5, None
    elif model == "naive_bayes":
        if name:
            return 10, "Naive Bayes"
        return 10, None
    elif model == "catboost":
        if name:
            return 15, "CatBoost"
        return 15, None
    else:
        return 0, None

if __name__ == '__main__':
    app.run(debug=True)