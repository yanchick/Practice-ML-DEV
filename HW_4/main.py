from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import os
import secrets
import csv
import psycopg2
from datetime import datetime

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_hex(16)
        self.db_params = {
            'dbname': 'web', # your db name 
            'user': 'postgres', # your username 
            'password': '123456:', # your password 
            'host': 'localhost' # your host 
        }
        self.query_get_history = 'SELECT input_data, model_used, output_data, predicted_at FROM "Prediction" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s) ORDER BY predicted_at DESC'
        self.category_mapping = {}
        self.models = {}
        self.model_names = ["catboost", "log_reg", "naive_bayes"]
        self.load_category_mapping()
        self.load_models()

        self.tfidf = None
        self.load_tfidf()

        self.setup_routes()

    def execute_query(self, query, params=None, fetch_one=False):
        connection = psycopg2.connect(**self.db_params)
        cursor = connection.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        except Exception as e:
            result = None

        connection.commit()
        cursor.close()
        connection.close()

        return result or []

    def load_category_mapping(self):
        with open("models/processed_pricerunner_aggregate.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_id = int(row['Category_ID'])
                if category_id in self.category_mapping:
                    continue
                category_label = row['Category_Label']
                self.category_mapping[category_id] = category_label

    def load_models(self):
        for model_name in self.model_names:
            model_path = os.path.join("models", f"{model_name}.pkl")
            with open(model_path, "rb") as file:
                self.models[model_name] = pickle.load(file)

    def load_tfidf(self):
        tfidf_path = "models/tfidf.pkl"
        with open(tfidf_path, "rb") as file:
            self.tfidf = pickle.load(file)

    def setup_routes(self):
        self.app.route('/')(self.index)
        self.app.route('/login', methods=['GET', 'POST'])(self.login)
        self.app.route('/register', methods=['GET', 'POST'])(self.register)
        self.app.route('/account_info')(self.account_info)
        self.app.route('/change_password', methods=['POST'])(self.change_password)
        self.app.route('/delete_account')(self.delete_account)
        self.app.route('/logout')(self.logout)
        self.app.route('/recharge', methods=['GET', 'POST'])(self.recharge)
        self.app.route('/make_prediction', methods=['POST'])(self.make_prediction)

    def run(self):
        self.app.run(debug=True)

    def index(self):
        if 'username' in session:
            query_get_user = 'SELECT balance FROM "Users" WHERE username = %s'
            balance = self.execute_query(query_get_user, (session['username'],), fetch_one=True)[0]
            
            return render_template('dashboard.html', username=session['username'], balance=balance)

        return redirect(url_for('login'))

    def login(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            query = 'SELECT * FROM "Users" WHERE username = %s AND password_hash = %s'
            result = self.execute_query(query, (username, password), fetch_one=True)

            if result:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid credentials')
        return render_template('login.html', error=None)

    def register(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            query_check_user = 'SELECT * FROM "Users" WHERE username = %s'
            existing_user = self.execute_query(query_check_user, (username,), fetch_one=True)

            if existing_user:
                flash('Username is already taken. Please choose another one.', 'error')
                return redirect(url_for('register'))
            
            if not (len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isupper() for c in password)):
                flash('Password must be at least 8 characters long and contain letters, numbers, and uppercase characters.', 'error')
                return redirect(url_for('register'))

            query_create_user = 'INSERT INTO "Users" (created_at, username, password_hash, balance) VALUES (%s,%s, %s, %s) RETURNING id_user'
            user_id = self.execute_query(query_create_user, (datetime.now(),username, password, 100), fetch_one=True)[0]

            query_get_balance = 'INSERT INTO "Billing_updating" (id_user, balance, updated_at) VALUES (%s, %s, %s)'
            result = self.execute_query(query_get_balance, (user_id, 100, datetime.now()), fetch_one=True)
            if result:
                _ = result[0]
            session['username'] = username

            flash('Registration successful. Welcome to the application!', 'success')

            return redirect(url_for('index'))

        return render_template('register.html')
        
    def account_info(self):
        if 'username' in session:
            # Get user information
            query_user_info = 'SELECT * FROM "Users" WHERE username = %s'
            user_info = self.execute_query(query_user_info, (session['username'],), fetch_one=True)

            # Get prediction history
            prediction_history = self.execute_query(self.query_get_history, (session['username'],))

            # Get transaction history
            query_transaction_history = 'SELECT balance_changed, operation_type, final_balance, changed_at FROM "Billing_history" WHERE id_user = %s ORDER BY changed_at DESC'
            transaction_history = self.execute_query(query_transaction_history, (user_info[0],))

            # Get last balance
            query_last_balance = 'SELECT * FROM "Billing_updating" WHERE id_user = %s'
            last_balance = self.execute_query(query_last_balance, (user_info[0],), fetch_one=True)

            return render_template('account_info.html', username=session['username'], user_info=user_info,
                                prediction_history=prediction_history, transaction_history=transaction_history,
                                last_balance=last_balance)

        return redirect(url_for('login'))
        
    def change_password(self):
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # Verify that the old password matches the stored password for the user
            query_check_password = 'SELECT * FROM "Users" WHERE username = %s AND password_hash = %s'
            result = self.execute_query(query_check_password, (session['username'], old_password), fetch_one=True)

            if result:
                if not (len(new_password) >= 8 and any(c.isalpha() for c in new_password) and any(c.isdigit() for c in new_password) and any(c.isupper() for c in new_password)):
                    flash('Password must be at least 8 characters long and contain letters, numbers, and uppercase characters.', 'error')
                else:
                    if new_password == confirm_password:
                        # Update the password in the database
                        query_update_password = 'UPDATE "Users" SET password_hash = %s WHERE username = %s'
                        _ = self.execute_query(query_update_password, (new_password, session['username']))

                        flash('Password changed successfully!', 'success')
                    else:
                        flash('New password and confirm password do not match.', 'error')
            else:
                flash('Incorrect old password.', 'error')

        return redirect(url_for('account_info'))

    def delete_account(self):
        if 'username' in session:

            query_delete_prediction = 'DELETE FROM "Prediction" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
            _ = self.execute_query(query_delete_prediction, (session['username'],))

            query_delete_billing_updating = 'DELETE FROM "Billing_updating" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
            _ = self.execute_query(query_delete_billing_updating, (session['username'],))

            query_delete_billing_history = 'DELETE FROM "Billing_history" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
            _ = self.execute_query(query_delete_billing_history, (session['username'],))

            query_delete_user = 'DELETE FROM "Users" WHERE username = %s'
            _ = self.execute_query(query_delete_user, (session['username'],))

            session.pop('username', None)
            return redirect(url_for('login'))
        return redirect(url_for('login'))

    def logout(self):
        session.pop('username', None)
        return redirect(url_for('login'))

    def recharge(self):
        if 'username' in session:
            if request.method == 'POST':
                amount = int(request.form['amount'])

                query_update_balance_updating = 'UPDATE "Billing_updating" SET balance = balance + %s, updated_at = %s WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
                _ = self.execute_query(query_update_balance_updating, (amount, datetime.now(), session['username']))

                query_update_balance_users = 'UPDATE "Users" SET balance = balance + %s WHERE username = %s'
                _ = self.execute_query(query_update_balance_users, (amount, session['username']))

                query_insert_history = 'INSERT INTO "Billing_history" (id_user, balance_changed, operation_type, final_balance, changed_at) VALUES ((SELECT id_user FROM "Users" WHERE username = %s), %s, %s, (SELECT balance FROM "Users" WHERE username = %s), %s)'
                _ = self.execute_query(query_insert_history, (session['username'], amount, '+', session['username'], datetime.now()), fetch_one=True)

            query_get_balance = 'SELECT balance FROM "Billing_updating" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
            balance = self.execute_query(query_get_balance, (session['username'],), fetch_one=True)[0]

            return render_template('dashboard.html', username=session['username'], balance=balance)
        return redirect(url_for('login'))

    def make_prediction(self):
        if 'username' in session:
            if request.method == 'POST':
                input_description = request.form['input_description']
                selected_model = request.form['selected_model']

                loaded_model = self.models.get(selected_model)

                if loaded_model is not None:
                    price, model_name = self.get_price(selected_model)
                    query_get_balance = 'SELECT balance FROM "Billing_updating" WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
                    user_balance = self.execute_query(query_get_balance, (session['username'],), fetch_one=True)[0]

                    if user_balance < price:
                        error_message = "Insufficient credits. Please recharge your balance."
                        return render_template('dashboard.html', username=session['username'], balance=user_balance, error=error_message)

                    input_description_tr = self.tfidf.transform([input_description])

                    prediction = loaded_model.predict(input_description_tr).item()
                    predicted_category = self.category_mapping.get(prediction, 'Other category')

                    query_update_balance_users = 'UPDATE "Users" SET balance = balance - %s WHERE username = %s'
                    _ = self.execute_query(query_update_balance_users, (price, session['username']))

                    query_update_balance = 'UPDATE "Billing_updating" SET balance = balance - %s, updated_at = %s WHERE id_user = (SELECT id_user FROM "Users" WHERE username = %s)'
                    _ = self.execute_query(query_update_balance, (price, datetime.now(), session['username']))

                    query_insert_history = 'INSERT INTO "Billing_history" (id_user, balance_changed, operation_type, final_balance, changed_at) VALUES ((SELECT id_user FROM "Users" WHERE username = %s), %s, %s, (SELECT balance FROM "Users" WHERE username = %s), %s)'
                    _ = self.execute_query(query_insert_history, (session['username'], price, '-', session['username'], datetime.now()), fetch_one=True)

                    query_insert_prediction = 'INSERT INTO "Prediction" (id_user, model_used, input_data, output_data, predicted_at, price) VALUES ((SELECT id_user FROM "Users" WHERE username = %s),%s, %s, %s, %s, %s)'
                    _ = self.execute_query(query_insert_prediction, (session['username'], model_name, input_description, predicted_category, datetime.now(), price), fetch_one=True)

                    _ = self.execute_query(self.query_get_history, (session['username'],))

                    return render_template('dashboard.html', username=session['username'], balance=user_balance - price, prediction=predicted_category, selected_model=model_name, price=price)
                else:
                    return render_template('dashboard.html', username=session['username'], balance=user_balance, error=f"Model {selected_model} not found")
        return redirect(url_for('login'))

    def get_price(self, model):
        if model == "log_reg":
            return 5, "Logistic Regression"
        elif model == "naive_bayes":
            return 10, "Naive Bayes"
        elif model == "catboost":
            return 15, "CatBoost"
        else:
            return 0, None

if __name__ == '__main__':
    web_app = WebApp()
    web_app.run()