import logging.config
from os import path
import os

from flask import jsonify
from flask import request
from flask import send_file
from flask import send_from_directory

from templategenerator.templategenerator import HelmTemplateGenerator

from . import create_app


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging_config.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger()


api = create_app()


CUSTOM_CONFIGS_DIRECTORY = "/tmp/custom-configs"


if not os.path.exists(CUSTOM_CONFIGS_DIRECTORY):
    os.makedirs(CUSTOM_CONFIGS_DIRECTORY)


@api.route("/create-template", methods=["POST"])
def create_template():
    """Creates a custom template."""
    email = request.form.get('email')
    password = request.form.get('password')
    org_name = request.form.get('org_name')
    jupyterhub_is_debug = request.form.get('jupyterhub_is_debug')
    jupyterhub_secret_tokena = request.form.get('jupyterhub_secret_token')
    jupyterhub_default_url = request.form.get('jupyterhub_default_url')
    singleuser_image = request.form.get('singleuser_image')
    singleuser_image_tag = request.form.get('singleuser_image_tag')
    is_auth_state_enabled = request.form.get('is_auth_state_enabled')
    auth_cryptokey = request.form.get('auth_cryptokey')
    is_admin_access = request.form.get('is_admin_access')
    admin_users = request.form.get('admin_users')
    authenticator_class = request.form.get('authenticator_class')
    jupyterhub_image = request.form.get('jupyterhub_image')
    jupyterhub_image_tag = request.form.get('jupyterhub_image_tag')
    jupyterhub_api_token = request.form.get('jupyterhub_api_token')
    auth_lti13_client_id = request.form.get('auth_lti13_client_id')
    auth_lti13_endpoint = request.form.get('auth_lti13_endpoint')
    auth_lti13_authorization_url = request.form.get('auth_lti13_authorization_url')
    auth_lti13_token_url = request.form.get('auth_lti13_token_url')
    postgres_nbgrader_password = request.form.get('postgres_nbgrader_password')
    postgres_nbgrader_host = request.form.get('postgres_nbgrader_host')
    postgres_jupyterhub_password = request.form.get('postgres_jupyterhub_password')
    postgres_jupyterhub_host = request.form.get('postgres_jupyterhub_host')
    postgres_jupyterhub_db = request.form.get('postgres_jupyterhub_db')
    postgres_jupyterhub_port = request.form.get('postgres_jupyterhub_port')
    jupyterhub_logofile_path = request.form.get('jupyterhub_logofile_path')
    jupyterhub_authenticator_class = request.form.get('jupyterhub_authenticator_class')
    is_efs_enabled = request.form.get('is_efs_enabled')
    efs_server_path = request.form.get('efs_server_path')
    is_nginx_ingress_enabled = request.form.get('is_nginx_ingress_enabled')
    nginx_ingress_host = request.form.get('nginx_ingress_host')
    is_postgresql_enabled = request.form.get('is_postgresql_enabled')
    postgres_username = request.form.get('postgres_username')
    postgres_password = request.form.get('postgres_password')
    postgres_database = request.form.get('postgres_database')
    is_gradersetupservice_enabled = request.form.get('is_gradersetupservice_enabled')
    gradersetupservice_image_name = request.form.get('gradersetupservice_image_name')
    grader_notebook_image_and_tag = request.form.get('grader_notebook_image_and_tag')
    postgres_nbgrader_user = request.form.get('postgres_nbgrader_user')
    # instantiate the template generator with vars from post data
    helm_template_generator = HelmTemplateGenerator(
        email,
        password,
        org_name,
        jupyterhub_is_debug ,
        jupyterhub_secret_tokena,
        jupyterhub_default_url,
        singleuser_image,
        singleuser_image_tag,
        is_auth_state_enabled,
        auth_cryptokey,
        is_admin_access,
        admin_users,
        authenticator_class,
        jupyterhub_image,
        jupyterhub_image_tag,
        jupyterhub_api_token,
        auth_lti13_client_id,
        auth_lti13_endpoint,
        auth_lti13_authorization_url,
        auth_lti13_token_url,
        postgres_nbgrader_password,
        postgres_nbgrader_host,
        postgres_jupyterhub_password,
        postgres_jupyterhub_host,
        postgres_jupyterhub_db,
        postgres_jupyterhub_port,
        jupyterhub_logofile_path,
        jupyterhub_authenticator_class,
        is_efs_enabled,
        efs_server_path,
        is_nginx_ingress_enabled,
        nginx_ingress_host,
        is_postgresql_enabled,
        postgres_username,
        postgres_password,
        postgres_database,
        is_gradersetupservice_enabled,
        gradersetupservice_image_name,
        grader_notebook_image_and_tag,
        postgres_nbgrader_user,
    )
    custom_config_file = helm_template_generator.create_custom_config_file()

    # write the file, then return it
    with open(os.path.join(CUSTOM_CONFIGS_DIRECTORY, custom_config_file), "wb") as fp:
        fp.write(custom_config_file)

    return send_file(custom_config_file)


@api.route("/files", methods=["GET"])
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(CUSTOM_CONFIGS_DIRECTORY):
        path = os.path.join(CUSTOM_CONFIGS_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>", methods=["GET"])
def get_file(path):
    """Download the template file."""
    return send_from_directory(CUSTOM_CONFIGS_DIRECTORY, path, as_attachment=True)


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Healtheck endpoint

    Returns:
        JSON: True if the service is alive
    """
    logger.debug("Health check reponse OK")
    return jsonify(success=True)


if __name__ == "__main__":
    api.run(host="0.0.0.0", debug=True)
