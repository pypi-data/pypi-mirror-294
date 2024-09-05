import attrs
from typing import Any
from pinecore import BaseObj
import tritonclient.grpc as grpcclient
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException


@attrs.define()
class Model(BaseObj):
  """
  
  """

  
