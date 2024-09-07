_A='retries'
import logging,os
from collections.abc import Callable
import requests
from localstack import config
from localstack.constants import API_ENDPOINT
from localstack.pro.core.bootstrap.auth import get_auth_headers
from localstack.utils.http import download,get_proxies
from localstack.utils.patch import patch
from localstack.utils.ssl import get_cert_pem_file_path,setup_ssl_cert
from localstack.utils.sync import retry
from localstack.utils.time import now
PLATFORM_CERTIFICATE_ENDPOINT_URL=f"{API_ENDPOINT}/certs"
PLATFORM_CERTIFICATE_ENDPOINT_TIMEOUT=5
PLATFORM_RETRY_CONFIG={_A:3,'sleep':1.}
CERTIFICATE_DOWNLOAD_TIMEOUT=5
CERTIFICATE_DOWNLOAD_RETRY_CONFIG={_A:3,'sleep':1.}
LOG=logging.getLogger(__name__)
def patch_setup_ssl_cert():
	@patch(target=setup_ssl_cert)
	def A(setup_community_ssl_cert):
		A=get_cert_pem_file_path()
		if os.path.exists(A):
			D=24*60*60;E=os.path.getmtime(A)
			if E>now()-D:LOG.debug('Using cached TLS certificate (less than 24 hrs since last update).');return
		LOG.debug('Attempting to download pro TLS certificate file');F=get_auth_headers();B=requests.Session();C=get_proxies()
		if C:B.proxies.update(C)
		def G():
			A=B.get(PLATFORM_CERTIFICATE_ENDPOINT_URL,timeout=PLATFORM_CERTIFICATE_ENDPOINT_TIMEOUT,headers=F)
			if not A.ok:raise Exception('Failed to download certificate, response code: %s',A.status_code)
			return A.json()['url']
		try:H=retry(G,**PLATFORM_RETRY_CONFIG);retry(download,url=H,path=A,timeout=CERTIFICATE_DOWNLOAD_TIMEOUT,quiet=True,**CERTIFICATE_DOWNLOAD_RETRY_CONFIG);LOG.debug('TLS certificate downloaded successfully to %s',A)
		except Exception:LOG.warning('Could not download custom per-organisation certificate, falling back to public certificate',exc_info=config.is_trace_logging_enabled());setup_community_ssl_cert()