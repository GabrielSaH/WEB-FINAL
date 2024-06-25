from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)
app.secret_key = "SáTanaz"


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html', user=session.get('nome'))

@app.route("/create-point")
def create_point():
    if session.get('id'):
        return render_template('create-point.html')
    return redirect('/login')        

@app.route('/search-results', methods=['POST'])
def search_results():
    search_form = request.form.get('search')
    possible_points = db.search_and_get_by_city(search_form)
    dic_of_points = db.make_dic_list(possible_points)

    return render_template('search-results.html', cards=dic_of_points)

@app.route('/submit', methods=['POST'])
def submit():
    # Extracting data from the form
    name = request.form.get('name')
    address = request.form.get('address')
    address2 = request.form.get('address2')
    state = request.form.get('uf')
    city = request.form.get('city')
    items = request.form.get('items')
    usr_id = session.get('id')
    # The DB cant have any entry with " or ', it would break the query

    name = name.replace("'", "")
    name = name.replace('"', '')
    
    address = address.replace("'", "")
    address = address.replace('"', '')

    city = city.replace("'", "")
    city = city.replace('"', '')

    items = items.replace(" ", "")
    items = items.replace(",", "")

    # Adding to the DB
    db.add_into_pontoColeta(name, address, address2, state, city, items, usr_id)

    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signin')
def signin():
    return render_template('registration.html')

@app.route('/sub_signin', methods=['POST'])
def signin_DB():
    # Retrieve form data using request.form dictionary
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirma_senha = request.form.get('confirma_senha')

    db.add_into_users(nome, cpf, email, senha)
    
    return  redirect('/login')

@app.route('/sub_login', methods=['POST'])
def login_DB():
    email = request.form.get('email')
    senha = request.form.get('senha')

    autenticado = db.check_password_email(email, senha)

    if autenticado:
        usr_info = db.get_user_info_by_email(email)
        session['nome'] = usr_info.get('nome')
        session['cpf'] = usr_info.get('cpf')
        session['id'] = usr_info.get('id')
        session['email'] = email
        return( redirect('/'))  
    else:
        error = 'email ou senha invalida'
        return render_template("login.html", error=error)
    
@app.route('/profile')
def profile_page():
    possible_points = db.search_by_usrID(session.get('id'))
    dic_of_points = db.make_dic_list(possible_points)

    return render_template('profile.html', cards=dic_of_points)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/edit')
def edit_point():
    name = request.args.get('name')
    addr1 = request.args.get('addr1')
    addr2 = request.args.get('addr2')
    state = request.args.get('state')
    city = request.args.get('city')
    id = request.args.get('id')

    card = {
        'name':    name,
        'addr1':   addr1,
        'addr2':   addr2,
        'state':   state,
        'city':    city,
        'id':      id
    }

    return render_template('edit-point.html', card = card)

@app.route('/sub_edit', methods = ['POST'])
def sub_edit():
    # Extracting data from the form
    name = request.form.get('name')
    address = request.form.get('address')
    address2 = request.form.get('address2')
    state = request.form.get('uf')
    city = request.form.get('city')
    items = request.form.get('items')
    usr_id = session.get('id')
    point_id = request.args.get('id')
    # The DB cant have any entry with " or ', it would break the query

    name = name.replace("'", "")
    name = name.replace('"', '')
    
    address = address.replace("'", "")
    address = address.replace('"', '')

    city = city.replace("'", "")
    city = city.replace('"', '')

    items = items.replace(" ", "")
    items = items.replace(",", "")

    return redirect('/')
