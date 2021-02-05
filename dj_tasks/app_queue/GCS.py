'''
this sc script is used to upload files to gcp cloud storage.
references:
Google github repo
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/storage_upload_file.py
'''
import io
import sys

# [START storage_upload_file]
from google.cloud import storage

class GCS:

    @staticmethod
    def upload_blob( bucket_name, src_file_name, tar_blob_name ):
        """Uploads a file to the bucket."""
        try:
            #
            storage_client = storage.Client()
            bucket = storage_client.bucket( bucket_name )
            blob = bucket.blob( tar_blob_name )

            blob.upload_from_filename( src_file_name )

            print(
                "File {} uploaded to {}.".format(
                    src_file_name, tar_blob_name
                )
            )
        except Exception as e:
            print( 'error uploading {}/{}, src:{}'.format( bucket_name, tar_blob_name, src_file_name ) )


    @staticmethod
    def upload_blob_from_string( bucket_name, src_string, tar_blob_name ):
        try:
            # Get the bucket that the file will be uploaded to.
            storage_client = storage.Client()
            bucket = storage_client.get_bucket( bucket_name )

            # Create a new blob and upload the file's content.
            my_file = bucket.blob( tar_blob_name )

            # create in memory file
            output = io.StringIO( src_string )

            # upload from string
            my_file.upload_from_string(output.read(), content_type="text/plain")

            output.close()

            # list created files
            blobs = storage_client.list_blobs(bucket)
            for blob in blobs:
                print(blob.name)

            # Make the blob publicly viewable.
            #my_file.make_public()
        
        except Exception as e:
            print( 'error uploading {}/{}, src_string: {}'.format( bucket_name, tar_blob_name , src_string ) )

    '''
    # test
    bucket_name = "aat_bk"
    src_file_name = "/home/canislatranscoxus/data/animals.txt"
    tar_blob_name = "animals.txt"
    upload_blob( bucket_name, src_file_name, tar_blob_name )
    bucket_name = "aat_bk"
    src_string = "vans \n airwalk \n nike \n"
    tar_blob_name = "skate/shoes.txt"
    upload_blob_from_string( bucket_name, src_string, tar_blob_name)'''