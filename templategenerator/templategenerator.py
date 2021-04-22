import logging
import logging.config
from os import path

from templategenerator.templates import HELM_CONFIG_TEMPLATE_V1


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging_config.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger()


class HelmTemplateException:
    """Custom helm template generator exception.
    """
    pass


class HelmTemplateGenerator:
    """Generates custom Helm config templates from template file versions."""
    def __init__(
        self,
        org_name: str,
        jupyterhub_is_debug: str,
        jupyterhub_secret_token: str,
        jupyterhub_default_url: str,
        singleuser_image: str,
        singleuser_image_tag: str,
        is_auth_state_enabled: str,
        auth_cryptokey: str,
        is_admin_access: str,
        admin_users: str,
        authenticator_class: str,
        jupyterhub_image: str,
        jupyterhub_image_tag: str,
        jupyterhub_api_token: str,
        auth_lti13_client_id: str,
        auth_lti13_endpoint: str,
        auth_lti13_authorization_url: str,
        auth_lti13_token_url: str,
        postgres_nbgrader_password: str,
        postgres_nbgrader_host: str,
        postgres_jupyterhub_password: str,
        postgres_jupyterhub_host: str,
        postgres_jupyterhub_db: str,
        postgres_jupyterhub_port: str,
        jupyterhub_logofile_path: str,
        jupyterhub_authenticator_class: str,
        is_efs_enabled: str,
        efs_server_path: str,
        is_nginx_ingress_enabled: str,
        nginx_ingress_host: str,
        is_postgresql_enabled: str,
        postgres_username: str,
        postgres_password: str,
        postgres_database: str,
        is_gradersetupservice_enabled: str,
        gradersetupservice_image_name: str,
        grader_notebook_image_and_tag: str,
        postgres_nbgrader_user: str,):
        """
        Instantiates class with variables needed for customization.

        Args:
          org_name: the organization name
          course_id: the course id

        Raises:
          HelmTemplateException the template could not be created.
        """
        self.org_name = org_name,
        self.jupyterhub_is_debug = jupyterhub_is_debug,
        self.jupyterhub_secret_tokena = jupyterhub_secret_token,
        self.jupyterhub_default_url = jupyterhub_default_url,
        self.singleuser_image = singleuser_image,
        self.singleuser_image_tag = singleuser_image_tag,
        self.is_auth_state_enabled = is_auth_state_enabled,
        self.auth_cryptokey = auth_cryptokey,
        self.is_admin_access = is_admin_access,
        self.admin_users = admin_users,
        self.authenticator_class = authenticator_class,
        self.jupyterhub_image = jupyterhub_image,
        self.jupyterhub_image_tag = jupyterhub_image_tag,
        self.jupyterhub_api_token = jupyterhub_api_token,
        self.auth_lti13_client_id = auth_lti13_client_id,
        self.auth_lti13_endpoint = auth_lti13_endpoint,
        self.auth_lti13_authorization_url = auth_lti13_authorization_url,
        self.auth_lti13_token_url = auth_lti13_token_url,
        self.postgres_nbgrader_password = postgres_nbgrader_password,
        self.postgres_nbgrader_host = postgres_nbgrader_host,
        self.postgres_jupyterhub_password = postgres_jupyterhub_password,
        self.postgres_jupyterhub_host = postgres_jupyterhub_host,
        self.postgres_jupyterhub_db = postgres_jupyterhub_db,
        self.postgres_jupyterhub_port = postgres_jupyterhub_port,
        self.jupyterhub_logofile_path = jupyterhub_logofile_path,
        self.jupyterhub_authenticator_class = jupyterhub_authenticator_class,
        self.is_efs_enabled = is_efs_enabled,
        self.efs_server_path = efs_server_path,
        self.is_nginx_ingress_enabled = is_nginx_ingress_enabled,
        self.nginx_ingress_host = nginx_ingress_host,
        self.is_postgresql_enabled = is_postgresql_enabled,
        self.postgres_username = postgres_username,
        self.postgres_password = postgres_password,
        self.postgres_database = postgres_database,
        self.is_gradersetupservice_enabled = is_gradersetupservice_enabled,
        self.gradersetupservice_image_name = gradersetupservice_image_name,
        self.grader_notebook_image_and_tag = grader_notebook_image_and_tag,
        self.postgres_nbgrader_user = postgres_nbgrader_user

    def create_custom_config_file(self):
        """Creates helm custom config from template
        """
        # Write the custom-config template file
        helm_custom_config_file = f'custom-onfig-{self.org_name}.yaml'
        logger.info(
            f'Writing template file: {helm_custom_config_file}'
        )
        # generate the file from template
        grader_home_nbconfig_content = HELM_CONFIG_TEMPLATE_V1.format(
            org_name = self.org_name,
            jupyterhub_is_debug = self.jupyterhub_is_debug,
            jupyterhub_secret_token = self.jupyterhub_secret_tokena,
            jupyterhub_default_url = self.jupyterhub_default_url,
            singleuser_image = self.singleuser_image,
            singleuser_image_tag = self.singleuser_image_tag,
            is_auth_state_enabled = self.is_auth_state_enabled,
            auth_cryptokey = self.auth_cryptokey,
            is_admin_access = self.is_admin_access,
            admin_users = self.admin_users,
            authenticator_class = self.authenticator_class,
            jupyterhub_image = self.jupyterhub_image,
            jupyterhub_image_tag = self.jupyterhub_image_tag,
            jupyterhub_api_token = self.jupyterhub_api_token,
            auth_lti13_client_id = self.auth_lti13_client_id,
            auth_lti13_endpoint = self.auth_lti13_endpoint,
            auth_lti13_authorization_url = self.auth_lti13_authorization_url,
            auth_lti13_token_url = self.auth_lti13_token_url,
            postgres_nbgrader_password = self.postgres_nbgrader_password,
            postgres_nbgrader_host = self.postgres_nbgrader_host,
            postgres_jupyterhub_password = self.postgres_jupyterhub_password,
            postgres_jupyterhub_host = self.postgres_jupyterhub_host,
            postgres_jupyterhub_db = self.postgres_jupyterhub_db,
            postgres_jupyterhub_port = self.postgres_jupyterhub_port,
            jupyterhub_logofile_path = self.jupyterhub_logofile_path,
            jupyterhub_authenticator_class = self.jupyterhub_authenticator_class,
            is_efs_enabled = self.is_efs_enabled,
            efs_server_path = self.efs_server_path,
            is_nginx_ingress_enabled = self.is_nginx_ingress_enabled,
            nginx_ingress_host = self.nginx_ingress_host,
            is_postgresql_enabled = self.is_postgresql_enabled,
            postgres_username = self.postgres_username,
            postgres_password = self.postgres_password,
            postgres_database = self.postgres_database,
            is_gradersetupservice_enabled = self.is_gradersetupservice_enabled,
            gradersetupservice_image_name = self.gradersetupservice_image_name,
            grader_notebook_image_and_tag = self.grader_notebook_image_and_tag,
            postgres_nbgrader_user = self.postgres_nbgrader_user,

        )
        return grader_home_nbconfig_content
