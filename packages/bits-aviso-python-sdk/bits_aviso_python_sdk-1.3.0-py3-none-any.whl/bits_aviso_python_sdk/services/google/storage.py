import google.auth.exceptions
import logging
from google.api_core import exceptions
from google.cloud import storage
from bits_aviso_python_sdk.services.google import authenticate_google_service_account
from bits_aviso_python_sdk.helpers.bigquery import parse_to_nldjson


class Storage:
	def __init__(self, service_account_credentials=None):
		"""Initializes the Storage class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.client = storage.Client(credentials=credentials)
		else:
			try:
				self.client = storage.Client()
			except google.auth.exceptions.DefaultCredentialsError as e:
				logging.error(f"Unable to authenticate service account. {e}")
				self.client = None

	def download_blob_to_file(self, bucket_name, blob_name, file_path, prefix=None):
		"""Downloads the specified blob to a file.

		Args:
			bucket_name (string): The name of the bucket.
			blob_name (string): The name of the blob.
			file_path (string): The path to save the downloaded file.
			prefix (string, optional): The prefix to use for the blob.

		Returns:
			string: The path to the downloaded file.

		Raises:
			ValueError: If the blob is not found in the bucket.
		"""
		try:
			# get the blob
			blob = self.get_blob(bucket_name, blob_name, prefix)
			# download the blob to the file
			logging.info(f"Downloading [{blob_name}] from {bucket_name} to [{file_path}]...")
			blob.download_to_filename(file_path)
			logging.info(f"Downloaded [{blob_name}] from {bucket_name} to [{file_path}].")

			return file_path

		except exceptions.NotFound:
			message = f"Blob [{blob_name}] not found in {bucket_name}."
			logging.error(message)

			raise ValueError(message)

	@staticmethod
	def create_blob(bucket, prefix, blob_name):
		"""Creates a blob in the specified bucket.

		Args:
			bucket (google.cloud.storage.bucket.Bucket): The bucket to create the blob in.
			prefix (string): The prefix to use for the blob. Typically, this is the name of the folder.
			blob_name (string): The name of the blob.

		Returns:
			google.cloud.storage.blob.Blob: The created blob.

		Raises:
			ValueError: If the bucket is not found.
		"""
		try:
			# create the blob
			logging.info(f"Creating blob {prefix}/{blob_name} in bucket {bucket}...")
			blob = bucket.blob(f"{prefix}/{blob_name}")
			logging.info(f"Created blob {prefix}/{blob_name} in bucket {bucket}.")

			return blob  # return the blob

		except exceptions.NotFound:
			message = f"Bucket {bucket} not found. Cannot proceed with creating blob {prefix}/{blob_name}."
			logging.error(message)

			raise ValueError(message)

	def get_blob(self, bucket_name, blob_name, prefix=None):
		"""Gets the specified blob.

		Args:
			bucket_name (string): The name of the bucket.
			blob_name (string): The name of the blob.
			prefix (string, optional): The prefix to use for the blob.


		Returns:
			google.cloud.storage.blob.Blob: The specified blob.

		Raises:
			ValueError: If the blob is not found in the bucket.
		"""
		# check if the prefix is provided
		if prefix:
			blob_name = f"{prefix}/{blob_name}"

		try:
			# get the bucket
			bucket = self.get_bucket(bucket_name)
			# get the blob from the bucket
			logging.info(f"Retrieving blob {blob_name} from {bucket_name}...")
			blob = bucket.blob(f"{blob_name}")

			return blob

		except exceptions.NotFound:
			message = f"Blob {blob_name} not found in {bucket_name}."
			logging.error(message)

			raise ValueError(message)

	def get_bucket(self, bucket_name):
		"""Gets the specified bucket.

		Args:
			bucket_name (string): The name of the bucket.

		Returns:
			google.cloud.storage.bucket.Bucket: The specified bucket.

		Raises:
			ValueError: If the bucket is not found.
		"""
		try:
			# get_bucket the bucket
			logging.info(f"Retrieving bucket {bucket_name}...")
			bucket = self.client.get_bucket(bucket_name)
			logging.info(f"Retrieved bucket {bucket_name}.")

			return bucket

		except exceptions.NotFound:
			message = f"Bucket {bucket_name} not found."
			logging.error(message)

			raise ValueError(message)

	def upload(self, bucket_name, prefix, blob_name, data, nldjson=False):
		"""Uploads the data to the specified bucket.

		Args:
			bucket_name (string): The name of the bucket.
			prefix (string): The prefix to use for the blob. Typically, the name of the dataset folder.
			blob_name (string): The name of the blob.
			data (str): The data to be uploaded to the bucket.
			nldjson (bool, optional): Whether to convert data to newline delimited json. Defaults to False.

		Raises:
			TypeError: If the data cannot be converted to newline delimited json.
			ValueError: If the data cannot be uploaded to the bucket.
		"""
		try:
			# get_bucket the bucket
			bucket = self.get_bucket(bucket_name)
			# create the blob
			blob = self.create_blob(bucket, prefix, blob_name)

			# check if the data needs to be converted to newline delimited json
			if nldjson:
				try:
					data = parse_to_nldjson(data)

				except TypeError:  # data is not a dictionary or a list of dictionaries, probably already converted
					raise ValueError("Unable to convert data to newline delimited json.")

			# upload the data
			logging.info(f"Uploading {prefix}/{blob_name} to {bucket_name}...")
			blob.upload_from_string(data)
			logging.info(f"Uploaded {prefix}/{blob_name} to {bucket_name}.")

		except ValueError as e:
			message = f"Unable to upload {blob_name} to {bucket_name}. {e}"
			logging.error(message)

			raise ValueError(message)  # raise an error with the message
