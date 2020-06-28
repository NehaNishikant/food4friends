from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
        'post_id': 1
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
        'post_id': 2
    }
]

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
result_iterable = container.query_items(query='SELECT * FROM Families f WHERE f.name="Piada"', enable_cross_partition_query=True)
results = list(result_iterable)

print(results[0]['address'])

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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
    return render_template('post.html', title="post.title", content="post")


if __name__ == '__main__':
    app.run(debug=True)
