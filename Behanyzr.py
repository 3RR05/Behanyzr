from App import create_app, db

app = create_app()

@app.cli.command()
def init_db():
    # Initializing DB
    
    db.create_all()
    print("DB Initialized! `~`")
    
if __name__ == '__main__':
    app.run(debug= True, host= '0.0.0.0', port= 5000)
