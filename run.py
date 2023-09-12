from app import app
import os
uploads_dir = os.path.join(os.getcwd(), 'uploads')

if __name__ == "__main__":
    app.run(debug=True)

if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)