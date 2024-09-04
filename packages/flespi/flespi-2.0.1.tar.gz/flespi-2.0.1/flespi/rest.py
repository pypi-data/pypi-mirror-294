"""Flespi REST API Class"""

import logging

import requests

log = logging.getLogger('flespi.rest.client')


class FlespiClient:
  """
  A helper client to work with Flespi REST API.
  """

  def __init__(self, token=''):
    """
    Constructor
    ...
    Attributes
    ----------
    token : str
      Flespi token, must be a Standard or Full-access token

    is_development : bool
      If True, prints request and parameters to console
      Deprecation warning: Will be removed in future versions, now the logging will work
                           with the standard Python logging module, with DEBUG level
    """
    self._token = token
    self._url = 'https://flespi.io'

  @property
  def _headers(self):
    """Headers"""
    return {'Accept': 'application/json', 'Authorization': f'FlespiToken {self._token}'}

  def get(self, method):
    """
    Perform a GET request to the Flespi API.
    ...
    Attributes
    ----------
    method : str
      The method to call with the namespace
      (i.e. '/gw/devices', where '/gw' is the namespace and '/devices' is the method)
    """

    url = self._url + method
    self._log_request(method)

    try:
      request = requests.get(
        url,
        headers=self._headers,
      )
      return self._validate_and_return(request)
    except requests.exceptions.RequestException as err:
      log.fatal('GET request failed: %s', err)
      return {'error': True, 'reason': err}

  def post(self, method, params):
    """
    Perform a POST request to the Flespi API.
    ...
    Attributes
    ----------
    method : str
      The method to call with the namespace
      (i.e. '/gw/devices', where '/gw' is the namespace and '/devices' is the method)
    params : dict
      A dictionary with key and params (i.e. {'name': 'Test'})
    """

    url = self._url + method
    self._log_request(method, params)

    try:
      request = requests.post(
        url,
        headers=self._headers,
        json=params,
      )
      return self._validate_and_return(request)
    except requests.exceptions.RequestException as err:
      log.fatal('POST request failed: %s', err)
      return {'error': True, 'reason': err}

  def put(self, method, params):
    """
    Perform a PUT request to the Flespi API.
    ...
    Attributes
    ----------
    method : str
      The method to call with the namespace
      (i.e. '/gw/devices', where '/gw' is the namespace and '/devices' is the method)
    params : dict
      A dictionary with key and params (i.e. {'name': 'Test'})
    """

    url = self._url + method
    self._log_request(method, params)

    try:
      request = requests.put(
        url,
        headers=self._headers,
        json=params,
      )
      return self._validate_and_return(request)
    except requests.exceptions.RequestException as err:
      log.fatal('PUT request failed: %s', err)
      return {'error': True, 'reason': err}

  def delete(self, method):
    """
    Perform a DELETE request to the Flespi API.
    ...
    Attributes
    ----------
    method : str
      The method to call with the namespace
      (i.e. '/gw/devices', where '/gw' is the namespace and '/devices' is the method)
    """

    url = self._url + method
    self._log_request(method)

    try:
      request = requests.delete(
        url,
        headers=self._headers,
      )
      return self._validate_and_return(request)
    except requests.exceptions.RequestException as err:
      log.fatal('DELETE request failed: %s', err)
      return {'error': True, 'reason': err}

  def _log_request(self, method, params=None):
    """
    Log request with DEBUG level
    Private method
    """
    log.debug('Request: %s - Params: %s', method, params)

  def _validate_and_return(self, request):
    """
    Validate the request and return the response with a dict object
    Private method
    """
    try:
      return {
        'error': request.status_code != 200,
        'code': request.status_code,
        'message': request.json(),
      }
    except ValueError:
      # log.fatal('Response validation failed: %s', err)
      return {
        'error': True,
        'reason': f'Invalid JSON response: {request.text}',
      }
