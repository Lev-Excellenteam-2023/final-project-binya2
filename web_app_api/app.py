import os
from datetime import datetime
import uuid
from flask import Flask, request, jsonify, json, make_response
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbManagement import Base, User, Upload

load_dotenv()
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = r"C:\exselentim\python\final-project-binya2\file_pro\uploads"
app.config["OUTPUT_FOLDER"] = r"C:\exselentim\python\final-project-binya2\file_pro\outputs"

def get_DB_session():
    engine = create_engine('sqlite:///../Database/db/mysqlite.sqlitedb')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
@app.route('/upload', methods=['POST'])
def upload() -> jsonify:
    """
    Handle file upload.
    """
    file = request.files['file']
    email = request.form.get('email')

    session = get_DB_session()

    user = None
    if email:
        if not session.query(User).filter_by(email=email).first():
            user = User(email=email)

    timestamp = datetime.now()
    uid = str(uuid.uuid4())
    upload_file = Upload(uid=uid,filename=file.filename.split('.')[0], upload_time=timestamp)
    upload_file.user = user
    session.add([upload_file, user])
    session.commit()
    session.close()

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{uid}"))

    return jsonify({'uid': uid})


@app.route('/status/<uid>', methods=['GET'])
def status() -> jsonify:
    """
    Get the status of a file.
    """
    uid = request.args.get('uid')
    email = request.args.get('email')
    filename = request.args.get('filename')
    matching_files = None
    session = get_DB_session()
    if uid:
        matching_files = session.query(Upload).filter_by(uid=uid).first()
    elif email:
        user = session.query(User).filter_by(email=email).first().first()
        matching_files = session.query(Upload).filter_by(user_id=user.id ,filename=filename).first()
    session.close()
    if not matching_files :
        return make_response(jsonify({'status': 'not found'}), 404)
    elif matching_files.status != 'done':
        return make_response(jsonify({'status': matching_files.status.value}), 200)
    else:
        return make_response(jsonify({'status': matching_files.status.value,
                        'filename': matching_files.filename,
                        'timestamp': matching_files.upload_time,
                        'explanation': matching_files.explanation}), 200)


if __name__ == '_main_':
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
       print("Creating upload folder")
    if not os.path.exists(app.config["OUTPUTS_FOLDER"]):
       print("Creating outputs folder")
    app.run()
