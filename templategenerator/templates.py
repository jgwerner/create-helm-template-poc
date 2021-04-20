HELM_CONFIG_TEMPLATE_V1 = """
jupyterhub:
  debug:
    enabled: {jupyterhub_is_debug}
  proxy:
    secretToken: {jupyterhub_secret_token}
  singleuser:
    storage:
      type: "static"
      static:
        pvcName: "shared-pvc-emory"
        subPath: {org_name}/home/{username}
      extraVolumeMounts:
        - name: home
          mountPath: /srv/nbgrader/exchange
          subPath: {org_name}/exchange/
    defaultUrl: {jupyterhub_default_url}
    image:
      name: {singleuser_image}
      tag: {singleuser_image_tag}
      pullPolicy: Always
  deploymentStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  auth:
    type: custom
    state:
      enabled: {is_auth_state_enabled}
      cryptoKey: {auth_cryptokey}
    admin:
      access: {is_admin_access}
      users:
        - {admin_users}
    custom:
      className: {authenticator_class}
  hub:
    image:
      name: {jupyterhub_image}
      tag: {jupyterhub_image_tag}
      pullPolicy: Always
    shutdownOnLogout: true
    extraEnv:
      JUPYTERHUB_API_TOKEN: {jupyterhub_api_token}
      JUPYTERHUB_API_URL: http://hub:8081/hub/api
      LTI13_CLIENT_ID: {auth_lti13_client_id}
      LTI13_ENDPOINT: {auth_lti13_endpoint}
      LTI13_AUTHORIZE_URL: {auth_lti13_authorization_url}
      LTI13_TOKEN_URL: {auth_lti13_token_url}
      LTI13_PRIVATE_KEY: '/srv/jupyterhub/rsa_private.key'
      POSTGRES_NBGRADER_USER: postgres
      POSTGRES_NBGRADER_PASSWORD: {postgres_nbgrader_password}
      POSTGRES_NBGRADER_HOST: {postgres_nbgrader_host}
      ORGANIZATION_NAME: {org_name}
      ILLUMIDESK_MNT_ROOT: '/illumidesk-courses'
      POSTGRES_JUPYTERHUB_USER: postgres
      POSTGRES_JUPYTERHUB_PASSWORD: {postgres_jupyterhub_password}
      POSTGRES_JUPYTERHUB_HOST:{postgres_jupyterhub_host}
      POSTGRES_JUPYTERHUB_DB: {postgres_jupyterhub_db}
      POSTGRES_JUPYTERHUB_PORT: {postgres_jupyterhub_port}
    extraConfig:
      logoConfig: |
        c.JupyterHub.logo_file = {jupyterhub_logofile_path}
      illumidesk.py: |
        import os
        from illumidesk.authenticators.authenticator import setup_course_hook
        from illumidesk.grades.handlers import SendGradesHandler
        c.JupyterHub.authenticator_class = {jupyterhub_authenticator_class}
        c.LTI13Authenticator.endpoint = os.environ.get('LTI13_ENDPOINT') or 'https://illumidesk.instructure.com/api/lti/security/jwks'
        c.LTI13Authenticator.client_id = os.environ.get('LTI13_CLIENT_ID') or ''
        c.LTI13Authenticator.authorize_url = os.environ.get('LTI13_AUTHORIZE_URL') or 'https://illumidesk.instructure.com/api/lti/authorize_redirect'
        c.LTI13Authenticator.token_url = os.environ.get('LTI13_TOKEN_URL') or 'https://illumidesk.instructure.com/login/oauth2/token'
        c.JupyterHub.extra_handlers = [
            (r'/lti13/config$', 'illumidesk.lti13.handlers.LTI13ConfigHandler'),
            (r'/lti13/jwks$', 'illumidesk.lti13.handlers.LTI13JWKSHandler'),
            (r'/submit-grades/(?P<course_id>[a-zA-Z0-9-_]+)/(?P<assignment_name>.*)$', SendGradesHandler),
          ]
        c.Authenticator.post_auth_hook = setup_course_hook
        def userdata_hook(spawner, auth_state):
            if not auth_state:
                raise ValueError('auth_state not enabled.')
            spawner.log.debug('auth_state_hook set with %s role' % auth_state['user_role'])
            user_role = auth_state['user_role']
            # set spawner environment
            spawner.environment['USER_ROLE'] = user_role
            spawner.log.debug("Assigned USER_ROLE env var to %s" % spawner.environment['USER_ROLE'])
        c.Spawner.auth_state_hook = userdata_hook
      illumideskSecurity: |
        c.JupyterHub.tornado_settings = {
          "headers": {"Content-Security-Policy": "frame-ancestors 'self' *"},
          "cookie_options": {"SameSite": "None", "Secure": True},
        }
      privateKey: |
        import os
        from os import chmod
        from Crypto.PublicKey import RSA
        key_path = os.environ.get('LTI13_PRIVATE_KEY') or '/srv/jupyterhub/rsa_private.key'
        key = RSA.generate(2048)
        with open(key_path, 'wb') as content_file:
          content_file.write(key.exportKey('PEM'))
        chmod(key_path, 0o600)

      illumideskServices: |
        import requests
        import os 
        c.JupyterHub.services.append({
          'name': 'announcement',
          'admin': True,
          'url': 'http://0.0.0.0:8889',
          'command': ["python3", "/etc/jupyterhub-services/announcement.py", "--port", "8889", "--api-prefix", "/services/announcement"],
          'api_token': 'dbd8cc4866eff335ab70ebd8337827663c1ab7319b7eb3c3453a9ad20002a0a0'})
        # load extra grader services launched from grader-setup service
        services_resp = requests.get('http://grader-setup-service.{}.svc.cluster.local:8000/services'.format(os.environ.get('ORGANIZATION_NAME')))
        services_resp = services_resp.json()
        c.JupyterHub.load_groups.update(services_resp['groups'])
        c.JupyterHub.services.extend(services_resp['services'])

allowNFS:
  enabled: {is_efs_enabled}
  server: {efs_server_path}
  path: /

nginxIngress:
  enabled: {is_nginx_ingress_enabled}
  host: {nginx_ingress_host}

postgresql:
  enabled: {is_postgresql_enabled}
  postgresqlUsername: {postgres_username}
  postgresqlPostgresPassword: {postgres_password}
  postgresqlPassword: {postgres_password}
  postgresqlDatabase: {postgres_database}

graderSetupService:
  enabled: {is_gradersetupservice_enabled}
  graderImage: {gradersetupservice_image_name}
  graderSetupImage: {grader_notebook_image_and_tag}
  postgresNBGraderHost: {postgres_nbgrader_host}
  postgresNBGraderUser: {postgres_nbgrader_user}
  postgresNBGraderPassword: {postgres_nbgrader_password}
"""
