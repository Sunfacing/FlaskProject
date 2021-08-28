import pymysql
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, send_from_directory
from flask.helpers import url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
load_dotenv()

connection = pymysql.connect(
    host = os.getenv('host'),
    user = os.getenv('user'),
    passwd = os.getenv('passwd'),
    database = os.getenv('database'),
    cursorclass = pymysql.cursors.DictCursor
)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif'])

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS `product` (\
                `id` int(11) AUTO_INCREMENT PRIMARY KEY,\
                `title` varchar(255),\
                `description` varchar(255),\
                `price` int(11),\
                `texture` varchar(255),\
                `wash` varchar(255),\
                `place` varchar(255),\
                `note` varchar(255),\
                `story` varchar(255)\
              )"
)

cursor.execute("CREATE TABLE IF NOT EXISTS `stock` (\
                `id` int(11) AUTO_INCREMENT PRIMARY KEY,\
                `product_id` int(11),\
                `color` varchar(255),\
                `color_code` varchar(255),\
                `size` varchar(255),\
                `stock` int(11),\
                FOREIGN KEY(product_id) REFERENCES product(id)\
              )"
)

cursor.execute("CREATE TABLE IF NOT EXISTS `campaign` (\
                `id` int(11) AUTO_INCREMENT PRIMARY KEY,\
                `product_id` int(11),\
                `title` varchar(255),\
                FOREIGN KEY(product_id) REFERENCES product(id)\
              )"
)

cursor.execute("CREATE TABLE IF NOT EXISTS `image` (\
                `id` int(11) AUTO_INCREMENT PRIMARY KEY,\
                `product_id` int(11),\
                `type` varchar(255),\
                `name` varchar(255),\
                FOREIGN KEY(product_id) REFERENCES product(id)\
              )"
)



def allowed_file(filename):
    """ Check img format is acceptable """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(product_id):
    """ Write Img info in to MYSQL and upload img in static/uploads """
    # Save main_img
    img_collections = ['imgs[]', 'main_img[]']
    for type in img_collections:
        imgs = request.files.getlist(type)
        for file in imgs:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                query = "INSERT INTO `image` (`product_id`, `type`, `name`) VALUES (%s, %s, %s)"
                cursor.execute(query, (product_id, type[:-2], filename))
                connection.commit()

    return redirect(url_for('product'))



def search_id():
    cursor.execute("SELECT * FROM product ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()['id']
     


def create_stock_by_color_size(form, product_id):
    i = 0
    while 'color'+str(i) in form:
        color = form[f'color{i}']
        color_code = form[f'Hex code{i}']
        size = form[f'size{i}']
        stock = form[f'stock{i}']
        print(color, color_code, size, stock, product_id)
        stock_query = "INSERT INTO `stock` (`product_id`, `color`, `color_code`, `size`, `stock`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(stock_query, (product_id, color, color_code, size, stock))
        i += 1
    connection.commit()
        



@app.route('/admin/product', methods=['GET', 'POST'])
def product():
    form = request.form
    if request.method == 'POST':
        title = form['title']
        description = form['description']
        price = form['price']
        texture = form['texture']
        wash = form['wash']
        place = form['place']
        note = form['note']
        story = form['story']

        # Create Basic Information
        product_query = "INSERT INTO `product` (`title`, `description`, `price`, `texture`, `wash`, `place`, `note`, `story` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(product_query, (title, description, price, texture, wash, place, note, story))
        connection.commit()

        # Create Stock Information
        product_id = search_id()

        # create_stock_by_color_size
        create_stock_by_color_size(form, product_id)

        # Save Image
        upload_image(product_id)
        
        return redirect(url_for('product'))
    else:
        return render_template('product.html')





@app.route('/<img>')
@app.route('/<int:img>')
def get_img(img=None):
    img = request.args.get('img', img)
    query = "SELECT name FROM stylish.image WHERE name = '{}'".format(img)
    if cursor.execute(query):
        image = cursor.fetchone()['name']
        return send_from_directory("static/uploads", image)

    return 'The image you request is not found'

if __name__ == '__main__':
    app.run(debug=True)