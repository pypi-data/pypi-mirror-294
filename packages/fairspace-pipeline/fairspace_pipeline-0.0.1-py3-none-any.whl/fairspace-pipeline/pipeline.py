import json
import logging
import os
import pathlib
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from api_client.fairspace_api_client import FairspaceApi
from graph.fairspace_graph import FairspaceGraph
from io_handler.io_handler_interface import IOHandlerInterface

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger('pipeline_main')


class PipelineConfig(BaseModel):
    source_study_prefixes: List[str] = Field(
        default_factory=lambda: json.loads(os.getenv('SOURCE_STUDIES_PREFIXES', '[""]')))
    output_data_directory: str = Field(
        default_factory=lambda: os.getenv('OUTPUT_DATA_PATH', os.path.join(os.getcwd(), 'test_data/.output_data')))
    is_aws_s3: bool = Field(default_factory=lambda: os.getenv("IS_AWS_S3", 'False').lower() in ('true', '1', 't'))
    source_study_directories: List[str] = Field(default_factory=list)
    source_bucket_name: Optional[str] = Field(default=None, env='AWS_SOURCE_BUCKET_NAME')
    output_bucket_name: Optional[str] = Field(default=None, env='AWS_OUTPUT_BUCKET_NAME')
    taxonomies_directory: str = Field(default_factory=lambda: os.getenv('TAXONOMIES_TTL_PATH', os.path.join(
        pathlib.Path(__file__).parent.absolute(), "config", "taxonomies.ttl")))
    taxonomy_namespace: str = Field(
        default_factory=lambda: os.getenv('TAXONOMY_NAMESPACE', 'https://fairspace.nl/ontology#'))
    fairspace_api_url: str = Field(default_factory=lambda: os.getenv('FAIRSPACE_API_URL'))
    keycloak_server_url: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_SERVER_URL'))
    keycloak_realm: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_REALM'))
    keycloak_client_id: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_CLIENT_ID'))
    keycloak_client_secret: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_CLIENT_SECRET'))
    keycloak_username: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_USERNAME'))
    keycloak_password: str = Field(default_factory=lambda: os.getenv('KEYCLOAK_PASSWORD'))
    verify_cert: bool = Field(
        default_factory=lambda: os.getenv('VERIFY_CERT', 'True').lower() not in ('false', '0', 'f'))


def load_config() -> PipelineConfig:
    try:
        config = PipelineConfig()
        config.source_study_directories = [os.path.join(os.getcwd(), val) for val in json.loads(
            os.getenv('SOURCE_STUDIES_PATHS', '["test_data/source_data"]'))] if not config.is_aws_s3 else json.loads(
            os.getenv('SOURCE_STUDIES_PATHS'))
        return config
    except ValidationError as e:
        print(f"Configuration error: {e}")
        raise


class Pipeline:
    def __init__(self, io_handler: IOHandlerInterface, fairspace_graph: FairspaceGraph):
        self.config = load_config()
        self.fairspace_graph = fairspace_graph
        self.io_handler = io_handler
        try:
            self.api = FairspaceApi(self.config.fairspace_api_url, self.config.keycloak_server_url,
                                    self.config.keycloak_realm, self.config.keycloak_client_id,
                                    self.config.keycloak_client_secret, self.config.keycloak_username,
                                    self.config.keycloak_password, self.config.verify_cert)
        except Exception as e:
            log.error(e)
            sys.exit(1)

    def prepare_current_user(self):
        user = self.api.get_current_user()
        self.api.update_user(user['id'], {'canQueryMetadata': 'true', 'canAddSharedMetadata': 'true'})

    def upload_taxonomies_to_fairspace(self):
        log.info('Updating taxonomies...')
        self.api.upload_metadata_by_path(self.config.taxonomies_directory)

    def reindex(self):
        log.info('Triggering recreation of a view database from the RDF database...')
        self.api.reindex()
        log.info("Reindexing started!")

    def run(self, init: bool = False, process: bool = False, upload: bool = False, delete: bool = False,
            reindex: bool = False, compact: bool = False, check_maintenance_status: bool = False):
        if init:
            self.prepare_current_user()
            self.upload_taxonomies_to_fairspace()
        if process:
            self.io_handler.transform_data(self.config.source_study_directories, self.config.source_study_prefixes)
        if upload:
            self.io_handler.send_to_api(self.api, self.config.source_study_directories)
        if delete:
            log.warning("Deletion not yet supported...")
        if reindex:
            self.reindex()
        if compact:
            self.api.compact()
        if check_maintenance_status:
            log.info("Maintenance status: " + self.api.maintenance_status())
        return True
