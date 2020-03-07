import numpy as np
from queue import Queue

class HeatMatrix:

   def __init__(self, shape, queue_size, origin=None):
      x,y = shape
      
      if x <= 1 | y <= 1:
         raise ValueTooSmallError
      
      if origin is not None:
         if origin[0] - x >= 0 or origin[1] - y >= 0:
            raise InvalidOriginError
         self.origin = origin
      else:
         self.origin = np.array([x // 2, y // 2]) 

      #CHANGE TO RESOLUTION
      self.shape = shape
      self.queue_size = queue_size
      self.frames_queue = Queue(self.queue_size)
      self.heat_matrix = np.zeros(self.shape)
      self.capacity = 0

   def _get_oldest_frame(self):
      oldest_frame = self.frames_queue.get()
      return oldest_frame

   def _add_new_frame(self, frame):
      self.capacity += 1
      self.frames_queue.put(frame)

   def _update_heat_matrix(self, new_frame):
      #Calculate overall decay being applied to a frame during its life time
      oldest_frame_decay = .5**self.queue_size
      
      # Check queue is full
      if self.capacity >= self.queue_size:
          #Decay the heat matrix data and then subtract the oldest frame
          self.heat_matrix = self.heat_matrix * .5 - (self._get_oldest_frame()*oldest_frame_decay)
      #Add the new data to the heat matrix
      self.heat_matrix += new_frame
      #Add newest frame into our queue for the future
      self._add_new_frame(new_frame)

   def compute_vector(self, new_frame):
      
      #Update the heatmatrix with the new frame
      self._update_heat_matrix(new_frame)

      #Get co-ordinate of highest value in heat_matrix
      highest_cord = np.unravel_index(np.argmax(self.heat_matrix, axis=None), self.heat_matrix.shape)
      
      #calculate the vector as (x1-x2),(y1-y2)
      #x1 and y1 being equivalent to origin
      vector = self.origin - highest_cord

      return vector

class ValueTooSmallError(Exception):
   """Raised when the input value is too small"""
   pass

class InvalidOriginError(Exception):
   """Raised when origin is outside of matrix"""
   pass
