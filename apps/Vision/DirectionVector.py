import numpy as np

class DirectionVector:

   def __init__(self):
      self.frames_queue = queue.Queue(5)
      self.shape = 2
      self.heat_matrix = np.ones(self.shape,self.shape)

   def get_oldest_frame(self):
      oldest_frame = self.frames_queue.get()
      return oldest_frame

   def add_new_frame(self, frame):
      self.frames_queue.put(frame)

   def compute_heat_matrix(self, new_frame):

      #Compute heat matrix by by removing data from the last frame (divide)
      #and add new frame (multiply)
      heat_matrix = (self.heat_matrix / self.get_oldest_frame()) * new_frame

      #Add newest frame into our queue for the future
      self.add_new_frame(new_frame)
   
      return heat_matrix

   def compute_vector(self, new_frame):
      
      #Compute Newest heat matrix
      heat_matrix = self.compute_heat_matrix(new_frame)
      
      #Get co-ordinate of highest value in heat_matrix
      highest_cord = np.unravel_index(heat_matrix.argmax(), heat_matrix.shape)
      
      #calculate the vector as (x1-x2),(y1-y2)
      vector = [self.shape/2,self.shape/2] - highest_cord
      return vector
