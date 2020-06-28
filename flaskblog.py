

from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family
import requests
import json

# Initialize the Cosmos client
endpoint = "https://neha-ashna-sql.documents.azure.com:443/"
key = 'OHGmnmv3z53vl7kn2r17rN9Suu20osDAfl4ALISjWO58biTjiLuldIdfsRdBA6IRnZFcczu7nrSEpHry6rLZew=='

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'AshnaNehaRestaurants'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'Restaurants'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/name"),
    offer_throughput=400
)
# </create_container_if_not_exists>


# Add items to the container
family_items_to_create = [family.thaiandnoodleoutlet(), family.piada(), family.allindia()]

 # <create_item>
for family_item in family_items_to_create:
    try:
        container.create_item(body=family_item)
    except:
        print('exists already')
# </create_item>


query = { 'query': 'SELECT * FROM server s' }    

options = {} 
options['enableCrossPartitionQuery'] = True
options['maxItemCount'] = 2

container = client.get_database_client("AshnaNehaRestaurants").get_container_client("Restaurants")
result_iterable = container.query_items(query='SELECT * FROM Families f', enable_cross_partition_query=True)
results = list(result_iterable)
address1 = results[0]['address']
address2 = results[1]['address']

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



posts = [
    {
        'author': 'Food4Friends',
        'title': 'Thai and Noodle Outlet',
        'content': 'Click above to learn more and/or donate',
        'date_posted': 'June 28, 2020',
        'post_id': 1,
        'address': address1
    },
    {
        'author': 'Food4Friends',
        'title': 'Piada',
        'content': 'Click above to learn more and/or donate',
        'date_posted': 'June 28, 2020',
        'post_id': 2,
        'address': address2
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    content = "Hey there! Welcome to Food4Friends by Ashna Mediratta and Neha Nishikant. We launched this project in response to Covid19. Due to the virus, food insecurity as increased. On the other hand, local businesses are suffering from less traffic. We created Food4Friends to harness the power of the people to fix both problems by bringing them together! You can pick your favorite local restaurant and buy a meal from them which will automatically be donated to a nearby soupkitchen. It's a Win-Win scenario :) Please consider donating!"
    return render_template('about.html', title='About', content=content)


@app.route("/donated")
def donate():
    return render_template('donate.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    #IMPORTANT query in the title and the content of the post here!!!
    if (post_id == 1):
        title = "Thai and Noodle Outlet"
        content = "Featuring delicious noodles, soups, and more!"
    if (post_id == 2):
        title = "Piada"
        content = "Authentic italian wraps, pastas, and salads!"

    url1="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/delivery_quotes"
    pickup_address ="9 Bernadette Circle, Monmouth Junction, 08852"
    dropoff_address = "30 Providence Blvd, Kendall Park NJ, 08824"
    quote_params = {
        "dropoff_address": dropoff_address,
        "pickup_address": pickup_address
    }
    quote_req = requests.post(url1, params=quote_params, auth=('ea6f0581-b447-459e-98cc-5c7b22a27335', ''))
    if quote_req.status_code != 200:
        print("Error:", quote_req.status_code)

    var = quote_req.json()
    w = var['fee']

    return render_template('post.html', title=title, content=content, cost = w)


if __name__ == '__main__':
    app.run(debug=True)
