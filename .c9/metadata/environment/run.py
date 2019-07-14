{"filter":false,"title":"run.py","tooltip":"/run.py","undoManager":{"mark":30,"position":30,"stack":[[{"start":{"row":0,"column":0},"end":{"row":279,"column":24},"action":"remove","lines":["'''","    Table of Contents","","    1. Connection with mongo db database","    2. Mail configuration","    3. MAIN page","    4. LOGIN function","    5. REGISTER function","    6. Check users in session before each request","    7. LOGOUT function","    8. ADD RECIPE page","    9. INSERT RECIPE","    10. MEAL page","    11. EDIT recipe  function","    12. UPDATE recipe function","    13. DELETE recipe function","    14. SEARCH function","    15. CHOSE CATEGORY","    16. CONTACT FORM","","'''","","","","","","","import os","import json","from flask import Flask, render_template,redirect,request,session,g, url_for,flash","from flask_pymongo import PyMongo","import bcrypt","from bson.objectid import ObjectId","from flask_mail import Mail","from flask_mail import Message","","","# Connection with mongo db database","","app = Flask(__name__)","app.secret_key = os.urandom(24)","app.config[\"MONGO_DBNAME\"] = \"Appetite_food\"","app.config[\"MONGO_URI\"] = \"mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority\"","mongo = PyMongo(app)","","","# Mail configuration","","app.config.update(","    MAIL_SERVER='smtp.gmail.com',","    MAIL_PORT=587,","    MAIL_USE_TLS=True,","    MAIL_DEFAULT_SENDER=\"appetitefoodinfo@gmail.com\",","    MAIL_USERNAME =os.environ.get(\"MAIL_USERNAME\"),","    MAIL_PASSWORD = os.environ.get(\"MAIL_PASSWORD\")","    )","mail = Mail(app)","","","# MAIN page. ","    ","@app.route(\"/\", methods=['GET', 'POST'])","@app.route(\"/index\", methods=['GET', 'POST'])","def index():","    if request.method == \"POST\":","        # when  search button is clicked user is redirected to results.html","        if request.form.get('action') == 'search':","            searched_text =  request.form.get('search_input')","            # if input is empty error alert apears","            if searched_text == \"\":","                flash(\"Please enter text to search\",\"alert\")","                return redirect(url_for('index',","                                        user=g.user))","            else:","                return redirect(url_for('search', ","                                        search_text=searched_text))","                            ","        # redirect user to result.html page after category is changed","        else:","            choosen_category =  request.form.get('category_name')","            return redirect(url_for('chose_category', ","                                    choosen_category=choosen_category))","                    ","    return render_template(\"index.html\",","    recipes = mongo.db.recipes.find(),","    categories= mongo.db.categories.find(),","    user=g.user)","","","# LOGIN function","","@app.route('/login', methods = ['GET','POST'])","def login():","    users = mongo.db.users","    login_user = users.find_one({'name' : request.form.get('username')})","    # Password verification","    if login_user:","        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):","            session['username'] = request.form.get('username')","            flash('Welcome ','alert')","            return redirect(url_for('index'))","        else:","            flash('Invalid password !','alert')","            return redirect(url_for('index'))","    else:","        flash('Invalid username !','alert')","        return redirect(url_for('index'))","","  ","# REGISTER function","","@app.route('/register', methods=['POST', 'GET'])","def register():","    if request.method == 'POST':","        users = mongo.db.users","        existing_user = users.find_one({'name' : request.form.get('username')})","        ","        # Hashing password to don't keep it in plain text","        if existing_user is None:","            pw_hash = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())","            users.insert({'name' : request.form.get('username'), 'password' : pw_hash})","            session['username'] = request.form.get('username')","        else:","            flash('That username already exists!','alert')","            return redirect(url_for('index'))","    flash('You have been successfully registered ')","    return redirect(url_for('index'))","    ","","# Check users in session before each request","","@app.before_request","def before_request():","    g.user = None","    if 'username' in session:","        g.user = session['username']","        ","","# LOGOUT function","","@app.route('/logout')","def logout():","    session.pop('username', None)","    flash('You have been logged out','alert')","    return redirect(url_for('index'))","","","# ADD RECIPE page","","@app.route('/add_recipe')","def add_recipe():","    return render_template(\"add_recipe.html\", ","                          recipe =mongo.db.recipes.find(),","                          user=g.user)"," "," ","#  INSERT RECIPE","   ","@app.route('/insert_recipe', methods=['POST'])","def insert_recipe():","    recipes = mongo.db.recipes","    ","    # It takes all values from form about recipe and inserts them into mongo database","    that_recipe = {","        \"name\": request.form.get('name'),","        \"image\": request.form.get('image'),","        \"description\": request.form.get('description'),","        \"author\": request.form.get('author'),","        \"ingredient\":  request.form.to_dict(flat=False)[\"ingredient_name\"],","        \"step\":  request.form.to_dict(flat=False)[\"step_name\"]","    }","    recipes.insert_one(that_recipe)","    return redirect(url_for('index'))","    ","    ","# MEAL page","","@app.route('/<recipe_id>')","def about_recipe(recipe_id):","    return render_template('meal.html',","                            recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),","                            user=g.user)"," ","    ","# EDIT recipe  function","    ","@app.route('/edit_recipe/<recipe_id>')","def edit_recipe(recipe_id):","    the_recipe = mongo.db. recipes.find_one({'_id': ObjectId(recipe_id)})","    return render_template('edit_recipe.html',","                            recipe= the_recipe,","                            user=g.user)","","# UPDATE recipe function","","@app.route(\"/update_recipe/<recipe_id>\", methods=[\"POST\"])","def update_recipe(recipe_id):","    recipes = mongo.db.recipes","    recipes.update( {'_id': ObjectId(recipe_id)},","    {","        \"name\": request.form.get('name'),","        \"image\": request.form.get('image'),","        \"description\": request.form.get('description'),","        \"author\": request.form.get('author'),","        \"ingredient\":  request.form.to_dict(flat=False)[\"ingredient_name\"],","        \"step\":  request.form.to_dict(flat=False)[\"step_name\"]","    })","    return redirect(url_for('index'))","","","# DELETE recipe function","","@app.route(\"/delete_recipe/<recipe_id>\")","def delete_recipe(recipe_id):","    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})","    return redirect(url_for('index'))","    ","    ","# SEARCH function","    ","@app.route(\"/search/<search_text>\", methods=[\"GET\",\"POST\"])","def search(search_text):","    ","    # takes searched phrase and rendering all recipes which contain this phrase in their name","    mongo.db.recipes.create_index([(\"name\",\"text\")])","    query = ({ \"$text\": { \"$search\":search_text}})","    the_recipes = mongo.db.recipes.find(query)","    the_number = the_recipes.count()","    flash(' for word \"{}\" :'.format(search_text),'result')","    ","    return  render_template(\"results.html\",","                            categories= mongo.db.categories.find(),","                            recipes= the_recipes,","                            recipes_number = the_number,","                            user=g.user)"," ","    ","# CHOSE CATEGORY","","@app.route(\"/chose/<choosen_category>\", methods=[\"GET\",\"POST\"])","def chose_category(choosen_category):","    the_recipes = mongo.db.recipes.find({\"category\": choosen_category})","    the_number = the_recipes.count()","    flash(\"  in {} category:\".format(choosen_category),'result')","    ","    return  render_template(\"results.html\",","                            categories= mongo.db.categories.find(),","                            recipes_number = the_number,","                            recipes= the_recipes,  user=g.user)","    ","    ","# CONTACT FORM","","@app.route(\"/contact\",methods=[\"GET\", \"POST\"])","def contact():","    if request.method == \"POST\":","        name=request.form.get('name')","        email=message=request.form.get('email')","        phone=request.form.get('phone')","        message=request.form.get('message')","        ","        # Message template which is sended to website owner email","        msg = Message(\"Message\",","                      recipients=[\"appetitefoodinfo@gmail.com\"])","        msg.html = \" <p>Mail from :<strong> \" + name + \"</strong></p><p>\" + message + \"</p><p>My email: \"+ email + \"</p><p>My phone: \" + phone +\"</p>\"","        mail.send(msg)","        flash(\"Thank you for your message {}. We will respond as soon as possible.\".format(","            request.form[\"name\"]","        ))","        ","    return render_template(\"contact.html\",","                            user=g.user)","    ","    ",""," ","if __name__=='__main__':","    app.run(host=os.environ.get(\"IP\"),","            port=int(os.environ.get(\"PORT\")),","            debug=False)"],"id":95},{"start":{"row":0,"column":0},"end":{"row":279,"column":24},"action":"insert","lines":["'''","    Table of Contents","","    1. Connection with mongo db database","    2. Mail configuration","    3. MAIN page","    4. LOGIN function","    5. REGISTER function","    6. Check users in session before each request","    7. LOGOUT function","    8. ADD RECIPE page","    9. INSERT RECIPE","    10. MEAL page","    11. EDIT recipe  function","    12. UPDATE recipe function","    13. DELETE recipe function","    14. SEARCH function","    15. CHOSE CATEGORY","    16. CONTACT FORM","","'''","","","","","","","import os","import json","from flask import Flask, render_template,redirect,request,session,g, url_for,flash","from flask_pymongo import PyMongo","import bcrypt","from bson.objectid import ObjectId","from flask_mail import Mail","from flask_mail import Message","","","# Connection with mongo db database","","app = Flask(__name__)","app.secret_key = os.urandom(24)","app.config[\"MONGO_DBNAME\"] = \"Appetite_food\"","app.config[\"MONGO_URI\"] = \"mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority\"","mongo = PyMongo(app)","","","# Mail configuration","","app.config.update(","    MAIL_SERVER='smtp.gmail.com',","    MAIL_PORT=587,","    MAIL_USE_TLS=True,","    MAIL_DEFAULT_SENDER=\"appetitefoodinfo@gmail.com\",","    MAIL_USERNAME =os.environ.get(\"MAIL_USERNAME\"),","    MAIL_PASSWORD = os.environ.get(\"MAIL_PASSWORD\")","    )","mail = Mail(app)","","","# MAIN page. ","    ","@app.route(\"/\", methods=['GET', 'POST'])","@app.route(\"/index\", methods=['GET', 'POST'])","def index():","    if request.method == \"POST\":","        # when  search button is clicked user is redirected to results.html","        if request.form.get('action') == 'search':","            searched_text =  request.form.get('search_input')","            # if input is empty error alert apears","            if searched_text == \"\":","                flash(\"Please enter text to search\",\"alert\")","                return redirect(url_for('index',","                                        user=g.user))","            else:","                return redirect(url_for('search', ","                                        search_text=searched_text))","                            ","        # redirect user to result.html page after category is changed","        else:","            choosen_category =  request.form.get('category_name')","            return redirect(url_for('chose_category', ","                                    choosen_category=choosen_category))","                    ","    return render_template(\"index.html\",","    recipes = mongo.db.recipes.find(),","    categories= mongo.db.categories.find(),","    user=g.user)","","","# LOGIN function","","@app.route('/login', methods = ['GET','POST'])","def login():","    users = mongo.db.users","    login_user = users.find_one({'name' : request.form.get('username')})","    # Password verification","    if login_user:","        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):","            session['username'] = request.form.get('username')","            flash('Welcome ','alert')","            return redirect(url_for('index'))","        else:","            flash('Invalid password !','alert')","            return redirect(url_for('index'))","    else:","        flash('Invalid username !','alert')","        return redirect(url_for('index'))","","  ","# REGISTER function","","@app.route('/register', methods=['POST', 'GET'])","def register():","    if request.method == 'POST':","        users = mongo.db.users","        existing_user = users.find_one({'name' : request.form.get('username')})","        ","        # Hashing password to don't keep it in plain text","        if existing_user is None:","            pw_hash = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())","            users.insert({'name' : request.form.get('username'), 'password' : pw_hash})","            session['username'] = request.form.get('username')","        else:","            flash('That username already exists!','alert')","            return redirect(url_for('index'))","    flash('You have been successfully registered ')","    return redirect(url_for('index'))","    ","","# Check users in session before each request","","@app.before_request","def before_request():","    g.user = None","    if 'username' in session:","        g.user = session['username']","        ","","# LOGOUT function","","@app.route('/logout')","def logout():","    session.pop('username', None)","    flash('You have been logged out','alert')","    return redirect(url_for('index'))","","","# ADD RECIPE page","","@app.route('/add_recipe')","def add_recipe():","    return render_template(\"add_recipe.html\", ","                          recipe =mongo.db.recipes.find(),","                          user=g.user)"," "," ","#  INSERT RECIPE","   ","@app.route('/insert_recipe', methods=['POST'])","def insert_recipe():","    recipes = mongo.db.recipes","    ","    # It takes all values from form about recipe and inserts them into mongo database","    that_recipe = {","        \"name\": request.form.get('name'),","        \"image\": request.form.get('image'),","        \"description\": request.form.get('description'),","        \"author\": request.form.get('author'),","        \"ingredient\":  request.form.to_dict(flat=False)[\"ingredient_name\"],","        \"step\":  request.form.to_dict(flat=False)[\"step_name\"]","    }","    recipes.insert_one(that_recipe)","    return redirect(url_for('index'))","    ","    ","# MEAL page","","@app.route('/<recipe_id>')","def about_recipe(recipe_id):","    return render_template('meal.html',","                            recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),","                            user=g.user)"," ","    ","# EDIT recipe  function","    ","@app.route('/edit_recipe/<recipe_id>')","def edit_recipe(recipe_id):","    the_recipe = mongo.db. recipes.find_one({'_id': ObjectId(recipe_id)})","    return render_template('edit_recipe.html',","                            recipe= the_recipe,","                            user=g.user)","","# UPDATE recipe function","","@app.route(\"/update_recipe/<recipe_id>\", methods=[\"POST\"])","def update_recipe(recipe_id):","    recipes = mongo.db.recipes","    recipes.update( {'_id': ObjectId(recipe_id)},","    {","        \"name\": request.form.get('name'),","        \"image\": request.form.get('image'),","        \"description\": request.form.get('description'),","        \"author\": request.form.get('author'),","        \"ingredient\":  request.form.to_dict(flat=False)[\"ingredient_name\"],","        \"step\":  request.form.to_dict(flat=False)[\"step_name\"]","    })","    return redirect(url_for('index'))","","","# DELETE recipe function","","@app.route(\"/delete_recipe/<recipe_id>\")","def delete_recipe(recipe_id):","    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})","    return redirect(url_for('index'))","    ","    ","# SEARCH function","    ","@app.route(\"/search/<search_text>\", methods=[\"GET\",\"POST\"])","def search(search_text):","    ","    # takes searched phrase and rendering all recipes which contain this phrase in their name","    mongo.db.recipes.create_index([(\"name\",\"text\")])","    query = ({ \"$text\": { \"$search\":search_text}})","    the_recipes = mongo.db.recipes.find(query)","    the_number = the_recipes.count()","    flash(' for word \"{}\" :'.format(search_text),'result')","    ","    return  render_template(\"results.html\",","                            categories= mongo.db.categories.find(),","                            recipes= the_recipes,","                            recipes_number = the_number,","                            user=g.user)"," ","    ","# CHOSE CATEGORY","","@app.route(\"/chose/<choosen_category>\", methods=[\"GET\",\"POST\"])","def chose_category(choosen_category):","    the_recipes = mongo.db.recipes.find({\"category\": choosen_category})","    the_number = the_recipes.count()","    flash(\"  in {} category:\".format(choosen_category),'result')","    ","    return  render_template(\"results.html\",","                            categories= mongo.db.categories.find(),","                            recipes_number = the_number,","                            recipes= the_recipes,  user=g.user)","    ","    ","# CONTACT FORM","","@app.route(\"/contact\",methods=[\"GET\", \"POST\"])","def contact():","    if request.method == \"POST\":","        name=request.form.get('name')","        email=message=request.form.get('email')","        phone=request.form.get('phone')","        message=request.form.get('message')","        ","        # Message template which is sended to website owner email","        msg = Message(\"Message\",","                      recipients=[\"appetitefoodinfo@gmail.com\"])","        msg.html = \" <p>Mail from :<strong> \" + name + \"</strong></p><p>\" + message + \"</p><p>My email: \"+ email + \"</p><p>My phone: \" + phone +\"</p>\"","        mail.send(msg)","        flash(\"Thank you for your message {}. We will respond as soon as possible.\".format(","            request.form[\"name\"]","        ))","        ","    return render_template(\"contact.html\",","                            user=g.user)","    ","    ",""," ","if __name__=='__main__':","    app.run(host=os.environ.get(\"IP\"),","            port=int(os.environ.get(\"PORT\")),","            debug=False)"]}],[{"start":{"row":93,"column":26},"end":{"row":94,"column":0},"action":"insert","lines":["",""],"id":96},{"start":{"row":94,"column":0},"end":{"row":94,"column":4},"action":"insert","lines":["    "]},{"start":{"row":94,"column":4},"end":{"row":94,"column":5},"action":"insert","lines":["t"]},{"start":{"row":94,"column":5},"end":{"row":94,"column":6},"action":"insert","lines":["h"]},{"start":{"row":94,"column":6},"end":{"row":94,"column":7},"action":"insert","lines":["e"]}],[{"start":{"row":94,"column":7},"end":{"row":94,"column":8},"action":"insert","lines":["_"],"id":97},{"start":{"row":94,"column":8},"end":{"row":94,"column":9},"action":"insert","lines":["u"]},{"start":{"row":94,"column":9},"end":{"row":94,"column":10},"action":"insert","lines":["s"]},{"start":{"row":94,"column":10},"end":{"row":94,"column":11},"action":"insert","lines":["e"]},{"start":{"row":94,"column":11},"end":{"row":94,"column":12},"action":"insert","lines":["r"]}],[{"start":{"row":94,"column":12},"end":{"row":94,"column":13},"action":"insert","lines":[" "],"id":98},{"start":{"row":94,"column":13},"end":{"row":94,"column":14},"action":"insert","lines":["="]}],[{"start":{"row":95,"column":42},"end":{"row":95,"column":70},"action":"remove","lines":["request.form.get('username')"],"id":99}],[{"start":{"row":94,"column":14},"end":{"row":94,"column":15},"action":"insert","lines":[" "],"id":100}],[{"start":{"row":94,"column":15},"end":{"row":94,"column":43},"action":"insert","lines":["request.form.get('username')"],"id":101}],[{"start":{"row":95,"column":41},"end":{"row":95,"column":42},"action":"insert","lines":[" "],"id":102},{"start":{"row":95,"column":42},"end":{"row":95,"column":43},"action":"insert","lines":["t"]},{"start":{"row":95,"column":43},"end":{"row":95,"column":44},"action":"insert","lines":["h"]},{"start":{"row":95,"column":44},"end":{"row":95,"column":45},"action":"insert","lines":["e"]},{"start":{"row":95,"column":45},"end":{"row":95,"column":46},"action":"insert","lines":["_"]}],[{"start":{"row":95,"column":42},"end":{"row":95,"column":46},"action":"remove","lines":["the_"],"id":103},{"start":{"row":95,"column":42},"end":{"row":95,"column":50},"action":"insert","lines":["the_user"]}],[{"start":{"row":100,"column":27},"end":{"row":100,"column":28},"action":"insert","lines":["{"],"id":104},{"start":{"row":100,"column":28},"end":{"row":100,"column":29},"action":"insert","lines":["}"]}],[{"start":{"row":100,"column":30},"end":{"row":100,"column":31},"action":"insert","lines":["."],"id":105},{"start":{"row":100,"column":31},"end":{"row":100,"column":32},"action":"insert","lines":["f"]},{"start":{"row":100,"column":32},"end":{"row":100,"column":33},"action":"insert","lines":["o"]},{"start":{"row":100,"column":33},"end":{"row":100,"column":34},"action":"insert","lines":["r"]},{"start":{"row":100,"column":34},"end":{"row":100,"column":35},"action":"insert","lines":["m"]},{"start":{"row":100,"column":35},"end":{"row":100,"column":36},"action":"insert","lines":["a"]},{"start":{"row":100,"column":36},"end":{"row":100,"column":37},"action":"insert","lines":["t"]}],[{"start":{"row":100,"column":37},"end":{"row":100,"column":38},"action":"insert","lines":["("],"id":106}],[{"start":{"row":100,"column":38},"end":{"row":100,"column":39},"action":"insert","lines":[")"],"id":107}],[{"start":{"row":100,"column":38},"end":{"row":100,"column":39},"action":"insert","lines":["t"],"id":108},{"start":{"row":100,"column":39},"end":{"row":100,"column":40},"action":"insert","lines":["h"]},{"start":{"row":100,"column":40},"end":{"row":100,"column":41},"action":"insert","lines":["e"]}],[{"start":{"row":100,"column":38},"end":{"row":100,"column":41},"action":"remove","lines":["the"],"id":109},{"start":{"row":100,"column":38},"end":{"row":100,"column":46},"action":"insert","lines":["the_user"]}],[{"start":{"row":53,"column":19},"end":{"row":53,"column":20},"action":"insert","lines":[" "],"id":110}],[{"start":{"row":42,"column":26},"end":{"row":42,"column":134},"action":"remove","lines":["\"mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority\""],"id":111},{"start":{"row":42,"column":26},"end":{"row":42,"column":57},"action":"insert","lines":["os.environ.get(\"MAIL_USERNAME\")"]}],[{"start":{"row":42,"column":43},"end":{"row":42,"column":55},"action":"remove","lines":["AIL_USERNAME"],"id":112},{"start":{"row":42,"column":43},"end":{"row":42,"column":44},"action":"insert","lines":["O"]},{"start":{"row":42,"column":44},"end":{"row":42,"column":45},"action":"insert","lines":["N"]},{"start":{"row":42,"column":45},"end":{"row":42,"column":46},"action":"insert","lines":["G"]},{"start":{"row":42,"column":46},"end":{"row":42,"column":47},"action":"insert","lines":["O"]},{"start":{"row":42,"column":47},"end":{"row":42,"column":48},"action":"insert","lines":["_"]}],[{"start":{"row":42,"column":48},"end":{"row":42,"column":49},"action":"insert","lines":["U"],"id":113},{"start":{"row":42,"column":49},"end":{"row":42,"column":50},"action":"insert","lines":["R"]},{"start":{"row":42,"column":50},"end":{"row":42,"column":51},"action":"insert","lines":["I"]}],[{"start":{"row":260,"column":43},"end":{"row":261,"column":0},"action":"insert","lines":["",""],"id":114},{"start":{"row":261,"column":0},"end":{"row":261,"column":8},"action":"insert","lines":["        "]},{"start":{"row":261,"column":8},"end":{"row":261,"column":9},"action":"insert","lines":["f"]},{"start":{"row":261,"column":9},"end":{"row":261,"column":10},"action":"insert","lines":["l"]},{"start":{"row":261,"column":10},"end":{"row":261,"column":11},"action":"insert","lines":["a"]},{"start":{"row":261,"column":11},"end":{"row":261,"column":12},"action":"insert","lines":["s"]}],[{"start":{"row":261,"column":12},"end":{"row":261,"column":13},"action":"insert","lines":["h"],"id":115}],[{"start":{"row":261,"column":13},"end":{"row":261,"column":15},"action":"insert","lines":["()"],"id":116}],[{"start":{"row":261,"column":14},"end":{"row":261,"column":16},"action":"insert","lines":["\"\""],"id":117}],[{"start":{"row":261,"column":15},"end":{"row":261,"column":78},"action":"insert","lines":["thank you for your message. we will respond as soon as possible"],"id":118}],[{"start":{"row":261,"column":15},"end":{"row":261,"column":16},"action":"remove","lines":["t"],"id":119}],[{"start":{"row":261,"column":15},"end":{"row":261,"column":16},"action":"insert","lines":["T"],"id":120}],[{"start":{"row":261,"column":43},"end":{"row":261,"column":44},"action":"remove","lines":["w"],"id":121}],[{"start":{"row":261,"column":0},"end":{"row":261,"column":79},"action":"remove","lines":["        flash(\"Thank you for your message. e will respond as soon as possible\")"],"id":122},{"start":{"row":260,"column":43},"end":{"row":261,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":269,"column":9},"end":{"row":269,"column":10},"action":"insert","lines":[","],"id":130}],[{"start":{"row":269,"column":10},"end":{"row":269,"column":12},"action":"insert","lines":["\"\""],"id":131}],[{"start":{"row":269,"column":11},"end":{"row":269,"column":12},"action":"insert","lines":["a"],"id":132},{"start":{"row":269,"column":12},"end":{"row":269,"column":13},"action":"insert","lines":["l"]},{"start":{"row":269,"column":13},"end":{"row":269,"column":14},"action":"insert","lines":["e"]},{"start":{"row":269,"column":14},"end":{"row":269,"column":15},"action":"insert","lines":["r"]},{"start":{"row":269,"column":15},"end":{"row":269,"column":16},"action":"insert","lines":["t"]}]]},"ace":{"folds":[],"scrolltop":3262.3125,"scrollleft":0,"selection":{"start":{"row":269,"column":18},"end":{"row":269,"column":18},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":238,"state":"start","mode":"ace/mode/python"}},"timestamp":1563090509937,"hash":"cfc9583d5def0a37c5a1c96813bebae3e2f74d6b"}