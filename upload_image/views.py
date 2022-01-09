from flask.helpers import url_for
from flask.json import load
from flask.templating import render_template
from flask_login.utils import login_required
from werkzeug.utils import redirect, secure_filename
from app import app
from flask_login import current_user
from upload_image.model import Image, ImageForm
from upload_image.service import getImageById, getImageByNameAndId
import base64
@app.route('/api/image-list', methods=['GET'])
@login_required
def image_list():
	curUser = current_user.get_id()

	images = getImageById(curUser)
	imageList = [img.nameImg for img in images]
	return {
		"status": "success",
		"data": imageList
	}

@app.route('/api/image-list/<string:fileName>/download', methods=['GET'])
# @login_required
def image_download(fileName):
	curUser = current_user.get_id()
	if not curUser:
		return {
		"status": "error",
		"message": "Image not found"
	}
	print("curUser", curUser)
	image = getImageByNameAndId(curUser, fileName)
	data_str = image.dataImg.read()

	if image:
		return {
			"status": "success",
			"data": {
				"img_name": image.nameImg,
				"img_content": data_str.decode('ISO-8859-1')
			}
		}

	return {
		"status": "error",
		"message": "Image not found"
	}

@app.route('/api/upload-image', methods=['POST'])
@login_required
def uploadImage():
	form = ImageForm()


	if form.validate_on_submit():
		file = form.imageFile.data
		filename = secure_filename(file.filename)
		userId = current_user.get_id()

		image = Image(userId=userId, nameImg=filename, dataImg=file)
		image.save()
		return {
			"status": "success",
			"data": {
				"img_name": image.nameImg
			}
		}

	return {
		"status": "error",
		"message": form.errors
	}
