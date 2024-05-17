from app import app, db, socketio

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    socketio.run(app=app, debug=True)
