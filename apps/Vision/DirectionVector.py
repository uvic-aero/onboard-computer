
import numpy as np
from queue import Queue

class DirectionVector:

   def __init__(self, size, queue_size):
      if size < 1:
         raise Exception("Size too small")
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

   def _compute_heat_matrix(self, new_frame):

      #Compute heat matrix by by removing data from the last frame (divide)
      #and add new frame (multiply)
      heat_matrix = (self.heat_matrix / self._get_oldest_frame()) * new_frame

      #Add newest frame into our queue for the future
      self._add_new_frame(new_frame)
   
      return heat_matrix

   def compute_vector(self, new_frame):
      
      #Compute Newest heat matrix
      heat_matrix = self._compute_heat_matrix(new_frame)
      
      #Get co-ordinate of highest value in heat_matrix
      highest_cord = np.unravel_index(heat_matrix.argmax(), heat_matrix.shape)
      
      #calculate the vector as (x1-x2),(y1-y2)
      vector = [self.shape/2,self.shape/2] - highest_cord
      return vector
