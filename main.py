from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:gg@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)

    def __init__(self, title, content ):
        self.title = title
        self.content = content
        


###########################################################################
@app.route('/')
def index():

   return redirect('/blog') 


###########################################################################
@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        #blog_title = request.form['blog-title']
        blog_body = request.form['blog-text']
        blog_title = request.form['blog-title']
        title_error = ''
        body_error = ''

        if blog_title == '':
            title_error = "Please enter a blog title"

        if blog_body == '':
            body_error = "Please enter a blog entry"

        
        print("THIS IS WHAT BLOGCONTENT IS FROM /newpostROUTE", blog_body)

        if not body_error and not title_error:
            new_entry = Blog(blog_title, blog_body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('blog?id={}'.format(new_entry.id, new_entry.content))
        else:
           return render_template('newpost.html', title='New Entry', title_error=title_error, body_error=body_error, 
                blog_title=blog_title, blog_body=blog_body   )
        



    return render_template('newpost.html', title='New Entry')
        



###########################################################################
@app.route('/blog')
def display_blogs():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Blog.query.all()
        blog_content = request.args.get('blog-text')

        print("THIS IS WHAT BLOGCONTENT IS FROM /BLOG ROUTE", blog_content)


        return render_template('blog.html', posts=posts, title='Build-a-Blog', blog_content=blog_content)
    else:
        posts = Blog.query.get(blog_id)
        blog_content = request.args.get('blog-text')
        print("THIS IS WHAT BLOGCONTENT IS FROM /BLOG ROUTE", blog_content)

        return render_template('new_entry.html', posts=posts, title='Entry', blog_content=blog_content)



if __name__ == '__main__':
    app.run()
