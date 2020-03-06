import numpy as np
from queue import Queue

class HeatMatrix:

   def __init__(self, size, queue_size, origin=None):
      if size <= 1:
         raise ValueTooSmallError
      
      if origin is not None:
         if origin[0] - size >= 0 or origin[1] - size >= 0:
            raise InvalidOriginError
         self.origin = origin
      else:
         self.origin = np.array([size // 2,size // 2]) 

      self.shape = (size,size)
      self.queue_size = queue_size
      self.frames_queue = Queue(self.queue_size)
      self.heat_matrix = np.ones(self.shape)
      self._init_queue()

   def _get_oldest_frame(self):
      oldest_frame = self.frames_queue.get()
      return oldest_frame

   def _add_new_frame(self, frame):
      self.frames_queue.put(frame)

   def _init_queue(self):
      dummy_frame = np.ones(self.shape)
      for q in range(self.queue_size):
         self.frames_queue.put(dummy_frame)

   def _update_heat_matrix(self, new_frame):

      #Compute heat matrix by by removing data from the last frame (divide)
      #and add new frame (multiply)
      self.heat_matrix = (self.heat_matrix / self._get_oldest_frame()) * new_frame

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
