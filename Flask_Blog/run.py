from flaskblog import create_app  # 'create_app' is found in the __init__.py file


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    