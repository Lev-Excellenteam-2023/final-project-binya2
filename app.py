import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.dbManagement import Base, User, Upload

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = r"C:\exselentim\python\final-project-binya2\file_pro\uploads"
app.config["OUTPUT_FOLDER"] = r"C:\exselentim\python\final-project-binya2\file_pro\outputs"


def get_DB_session():
    engine = create_engine('sqlite:///Database/db/mysqlite.db')
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
    # email = None
    # file = None
    user = None
    session = get_DB_session()
    # logger.info(f"Uploading file: {file.filename} in: {datetime.now()} by: {email}")
    if email:
        if not session.query(User).filter_by(email=email).first():
            user = User(email=email)
            session.add(user)
            session.commit()

    timestamp = datetime.now()
    uid = str(uuid.uuid4())
    upload_file = Upload(uid=uid, filename=file.filename.split('.')[0], upload_time=timestamp)
    upload_file.user = user
    session.add(upload_file)
    session.commit()
    session.close()

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{uid}.pptx"))

    return jsonify({'uid': uid})


@app.route('/status/', methods=['GET'])
def status() -> jsonify:
    """
    Get the status of a file.
    """
    # email = None
    # filename = None
    email = request.args.get('email')
    filename = request.args.get('filename')
    uid = request.args.get('uid')
    matching_files = None
    session = get_DB_session()
    if uid:
        matching_files = session.query(Upload).filter_by(uid=uid).first()
    elif email:
        user = session.query(User).filter_by(email=email).first()
        matching_files = session.query(Upload).filter_by(user_id=user.id, filename=filename).first()
    if matching_files.uid is None:
        rsp =  make_response(jsonify({'status': 'not found'}),404)
    else:
        rsp = make_response(jsonify({'status': matching_files.status.value, 'filename': matching_files.filename,
                                     'upload_time': matching_files.upload_time,
                                     'finish_time': matching_files.finish_time}), 200)
    session.close()
    return rsp



if __name__ == '_main_':
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        print("Creating upload folder")
    if not os.path.exists(app.config["OUTPUTS_FOLDER"]):
        print("Creating outputs folder")
    app.run()
