"""
This module contains classes and functions for running Fairspace pipelines on AWS S3 buckets. It includes classes
for processing source files, writing ttl files, and uploading data to Fairspace.

Classes:
    AwsS3IOHandler: Class to handle running pipeline on AWS S3 buckets.

"""

import json
import logging
import pathlib
import sys
from typing import List

import boto3
from botocore.exceptions import NoCredentialsError
from rdflib import Graph

from api_client.fairspace_api_client import FairspaceApi
from graph.fairspace_graph import FairspaceGraph
from io_handler_interface import IOHandlerInterface

log = logging.getLogger('aws_s3_connector')

DEFAULT_BUCKET_PAGINATION_PAGE_SIZE = 10
STAGING_DIRECTORY_NAME = "fairspace-metadata-upload-staging"


class AwsS3IOHandler(IOHandlerInterface):
    """
    IOHandler implementation for interacting with AWS S3.

    This class provides methods for extraction, transformation and loading of data while interacting with AWS S3 bucket.
    """
    def __init__(self, source_bucket_name: str, output_bucket_name: str, fairspace_graph: FairspaceGraph, encoding = 'utf-8-sig'):
        super().__init__(fairspace_graph)
        session = boto3.Session(profile_name='default')
        self.s3_client = session.client('s3')
        self.source_bucket_name = source_bucket_name
        self.output_bucket_name = output_bucket_name
        self.encoding = encoding

    def transform_data(self, source_directories: str, source_prefixes: List[str] = []):
        try:
            for label_prefix in source_prefixes:
                if label_prefix != "":
                    log.info(f'Applying label prefix: "{label_prefix}".')
                for source_directory in source_directories:
                    data_path = f"{STAGING_DIRECTORY_NAME}/{label_prefix+source_directory}"
                    self.upload_to_aws(data_path + '/')
                    self.process_data(source_directory, label_prefix)
                    log.info(f'Done processing source files in {source_directory} folder.')
        except Exception as e:
            log.error(e)
            sys.exit(1)
        log.info(f'Done processing all the source files for configured directories.')

    def send_to_api(self, api: FairspaceApi, data_directories: list[str]):
        for data_path in data_directories:
            self.upload_files_to_fairspace_with_pagination(api, data_path)
        log.info(f"Done uploading all metadata from {self.output_bucket_name} bucket to Fairspace.")

    def write_to_ttl(self, graph: Graph, filename: str, output_directory: str, prefix: str = ""):
        new_file_name = prefix + pathlib.Path(filename).with_suffix('.ttl').name
        output = output_directory + "/" + new_file_name
        file = graph.serialize(format="turtle")
        self.upload_to_aws(output, file)

    def upload_files_to_fairspace_with_pagination(self, api: FairspaceApi, data_path: str):
        page_iterator = self.read_from_aws(self.output_bucket_name, data_path,
                                           DEFAULT_BUCKET_PAGINATION_PAGE_SIZE)
        for page in page_iterator:
            log.info(f"Getting {DEFAULT_BUCKET_PAGINATION_PAGE_SIZE} files from S3 {data_path} directory")
            files = page.get("Contents")
            for file in files:
                file_name = file['Key']
                self.upload_file_to_fairspace(api, file_name)

    def upload_file_to_fairspace(self, api: FairspaceApi, file_name: str):
        try:
            log.info(f"Start uploading file {file_name} to Fairspace")
            file_content = self.get_file_content(self.output_bucket_name, file_name)
            api.upload_metadata('turtle', file_content, False)
        except Exception as e:
            log.error(f"Error uploading file {file_name}")
            log.error(e)
            sys.exit(1)

    def process_data(self, data_directory: str, prefix: str):
        page_iterator = self.read_from_aws(self.source_bucket_name, data_directory, DEFAULT_BUCKET_PAGINATION_PAGE_SIZE)
        page_count = 0
        for page in page_iterator:
            log.info(f"Getting {DEFAULT_BUCKET_PAGINATION_PAGE_SIZE} files from page {page_count} of {data_directory}...")
            files = page.get("Contents")
            page_count = page_count+1
            for file in files:
                file_path = file['Key']
                try:
                    log.info(f"Processing file with name: {file_path}, size: {file['Size']}")
                    file_content = self.get_file_content(self.source_bucket_name, file_path)
                    data = json.loads(file_content)
                    data_graph = self.fairspace_graph.create_graph(file_path, data, prefix)
                    data_path = f"{STAGING_DIRECTORY_NAME}/{prefix + data_directory}"
                    self.write_to_ttl(data_graph, file_path, data_path, prefix)
                except Exception as e:
                    log.error(f"Error processing file with name {file_path}")
                    raise Exception(e)

    def upload_to_aws(self, s3_object_name: str, object_to_upload=None):
        try:
            if object_to_upload is not None:
                self.s3_client.put_object(Body=object_to_upload, Bucket=self.output_bucket_name, Key=s3_object_name)
            else:
                self.s3_client.put_object(Bucket=self.output_bucket_name, Key=s3_object_name)
            log.info(f"Successfully uploaded {s3_object_name} to {self.output_bucket_name} AWS S3 bucket.")
            return True
        except NoCredentialsError:
            log.error("AWS S3 bucket credentials not available.")
            raise Exception(NoCredentialsError)
        except Exception as e:
            log.error(f"Error uploading {s3_object_name} to {self.output_bucket_name} AWS S3 bucket.")
            raise Exception(e)

    def read_from_aws(self, bucket_name: str, path: str, page_size: int):
        paginator = self.s3_client.get_paginator("list_objects_v2")
        return paginator.paginate(Bucket=bucket_name, Prefix=path, PaginationConfig={"PageSize": page_size})

    def get_files_by_suffix(self, bucket_name: str, path: str, page_size: int, suffix: str):
        page_iterator = self.read_from_aws(bucket_name, path, page_size)
        files = page_iterator.search(f"Contents[?ends_with(Key, `{suffix}`)][]")
        return files

    def get_file_content(self, bucket_name: str, file_key: str):
        file_object = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = file_object['Body'].read().decode(self.encoding, errors="ignore")
        return file_content
