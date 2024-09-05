"""A wrapper for pycram_bullet to manage different clients."""
from __future__ import absolute_import
from __future__ import division
import os
import functools
import inspect
import pycram_bullet


class BulletClient(object):
  """A wrapper for pycram_bullet to manage different clients."""

  def __init__(self, connection_mode=None, hostName=None, options=''):
    """Creates a Bullet client and connects to a simulation.

    Args:
      connection_mode:
        `None` connects to an existing simulation or, if fails, creates a
          new headless simulation,
        `pycram_bullet.GUI` creates a new simulation with a GUI,
        `pycram_bullet.DIRECT` creates a headless simulation,
        `pycram_bullet.SHARED_MEMORY` connects to an existing simulation.
    """
    self._shapes = {}
    self._pid = os.getpid()
    if connection_mode is None:
      self._client = pycram_bullet.connect(pycram_bullet.SHARED_MEMORY, options=options)
      if self._client >= 0:
        return
      else:
        connection_mode = pycram_bullet.DIRECT
    if hostName is None:
        self._client = pycram_bullet.connect(connection_mode, options=options)
    else:
        self._client = pycram_bullet.connect(connection_mode, hostName=hostName, options=options)

  def __del__(self):
    """Clean up connection if not already done."""
    if self._client>=0 and self._pid == os.getpid():
      try:
        pycram_bullet.disconnect(physicsClientId=self._client)
        self._client = -1
      except pycram_bullet.error:
        pass

  def __getattr__(self, name):
    """Inject the client id into Bullet functions."""
    attribute = getattr(pycram_bullet, name)
    if inspect.isbuiltin(attribute):
      attribute = functools.partial(attribute, physicsClientId=self._client)
    if name=="disconnect":
      self._client = -1 
    return attribute
