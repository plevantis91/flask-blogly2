from flask import Flask, render_template, redirect, request, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hushhushhush'

app.debug = False 

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()  # Create tables if they don't exist
    print('Tables created')

@app.route('/')
def home():
    # Displays a page with the list of users
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/form', methods = ["GET","POST"])
def create_user():
    # Display page with the form to create a new user
    if request.method == 'POST':
        new_user = User(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            image_url=request.form.get('image_url' or None)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    
    return render_template('users/form.html')
        

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    #  Displays page with info of a specified users
    user = User.query.get_or_404(user_id)
    return render_template('/users/detail.html', user=user)
   

@app.route('/users/<int:user_id>/edit', methods = ['GET', 'POST'])
def edit_user(user_id):
    # Updates the user information
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template('/users/edit.html', user=user)
    elif request.method == 'POST':
        user = User.query.get_or_404(user_id)
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url')

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    # Deletes specified user
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

# Posts routes

@app.route('/users/<int:user_id>/post/form', methods = ['GET', 'POST'])
def create_post(user_id):
    # Creates new post by specified user
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template('posts/form.html', user=user, tags=tags)
    elif request.method == 'POST':
        user = User.query.get_or_404(user_id)
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(title=request.form.get('title'),
                        content=request.form.get('content'),
                        user=user,
                        tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post has been added.")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    # Displays page with info of a specified post 
    post = Post.query.get_or_404(post_id)
    return render_template('posts/detail.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    # Updates the post information
    if request.method == 'GET':
        post = Post.query.get_or_404(post_id)
        tags = Tag.query.all()
        return render_template('/posts/edit.html', post=post, tags=tags)
    elif request.method == 'POST':
        post = Post.query.get_or_404(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        tag_ids = [int(num) for num in request.form.getlist("posts")]
        post.tags = Post.query.filter(Post.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    # Deletes specified post
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

# Tag routes
@app.route('/tags')
def tags_list():
    # Displays page with list of tags
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/form', methods=['GET', 'POST'])
def create_tag():
    # Displays page with form to create a new tag
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('tags/form.html', posts=posts)
    elif request.method == 'POST':
      post_ids = [int(num) for num in request.form.getlist("posts")]
      posts = Post.query.filter(Post.id.in_(post_ids)).all()
      new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    # Displays page with info of a specified tag
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/detail.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    # Updates the tag information
    if request.method == 'GET':
        posts=Post.query.all()
        tag = Tag.query.get_or_404(tag_id)
        return render_template('/tags/edit.html', tag=tag, posts=posts)
    elif request.method == 'POST':
        tag = Tag.query.get_or_404(tag_id)
        tag.name = request.form.get('name')
        post_ids = [int(num) for num in request.form.getlist("posts")]
        tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    # Deletes specified tag
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')


if __name__ == '__main__':
   
    app.run(debug=True)