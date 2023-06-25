from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# File path to store the entries
entries_file = 'entries.txt'

# Set your desired password
password = 'password'

@app.route('/')
def index():
    entries = get_entries()
    formatted_entries = format_entries(entries)
    return render_template('index.html', entries=formatted_entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        entry_content = request.form['content']
        entry_password = request.form['password']

        if entry_password == password:
            save_entry(entry_content)
            return redirect('/')
        else:
            return "Invalid password. Entry not saved."

    return render_template('new_entry.html')

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    entry_id = request.form.get('entry_id')
    entry_password = request.form.get('password')

    if entry_id is None or entry_password is None:
        return "Invalid request. Entry not deleted."

    entries = get_entries()
    if not (1 <= int(entry_id) <= len(entries)):
        return "Invalid entry ID. Entry not deleted."

    if entry_password == password:
        delete_entry(int(entry_id))
        return redirect('/')
    else:
        return "Invalid password. Entry not deleted."

def save_entry(content):
    with open(entries_file, 'a') as file:
        file.write(content + '\n')

def delete_entry(entry_id):
    entries = get_entries()

    if 1 <= entry_id <= len(entries):
        del entries[entry_id - 1]

        with open(entries_file, 'w') as file:
            file.write('\n'.join(entries))

def get_entries():
    with open(entries_file, 'r') as file:
        entries = file.read().splitlines()
    return entries

def format_entries(entries):
    formatted_entries = []
    for i, entry in enumerate(entries, 1):
        formatted_entry = {
            'number': i,
            'date': get_entry_date(entry),
            'content': entry
        }
        formatted_entries.append(formatted_entry)
    return formatted_entries

def get_entry_date(entry):
    # Implement this function to retrieve the date for each entry
    # For now, let's return the current date and time as a placeholder
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True)
