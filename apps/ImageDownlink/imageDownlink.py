class ImageDownlink:
	def _save_image(self, image):
		cur_dir = os.path.dirname(__file__)
		photo_dir = os.path.join(cur_dir, 'images')
		photo_name = os.path.basename(str(time.time()) + '.jpg')
		photo_path = os.path.join(photo_dir, photo_name)

		if not os.path.exists(photo_dir):
			os.mkdir(photo_dir)

		# Save the image at .../picture folder
		with open(photo_path, 'wb') as f:
			f.write(image)

	def send_image(self, image):
	
		self._save_image(image)

		try:
			timestamp = time.time() * 1000
			#encoded_image = base64.b64encode(image)
			encoded_image = base64.b64encode(image)

			payload = {
				'timestamp': timestamp,
				'image': encoded_image.decode('utf-8', "ignore")
			}

			requests.post(groundstation_url + '/images', json=payload)

		except Exception as e:
			print(str(e))
			print("Failed to send image to groundstation")
