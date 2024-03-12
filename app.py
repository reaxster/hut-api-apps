from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5050)


   #TODO: Run flask shell
   # db.create_all()
   # to create table definition on startup