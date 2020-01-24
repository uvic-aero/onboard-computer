import numpy as np

class DirectionVector:

   def __init__(self):
      self.frames_queue = queue.Queue(5)
      self.shape = 2
      self.heat_matrix = np.ones(shape,shape)
      pass

   #Take in most recent frame and return the probability matrix
   def compute_heat_matrix(self, new_frame, frames_queue)
         #Take oldest frame out of the queue
         oldest_frame = frames_queue.get()

         #Compute heat matrix by by removing data from the last frame (divide)
         #and add new frame (multiply)
         heat_matrix = (heat_matrix / oldest_frame) * new_frame

         #Add newest frame into our queue for the future
         frames_queue.put(new_frame)
   
        return heat_matrix

   #only public method
   def compute_vector(self, frame)
      #Compute Newest heat matrix
      heat_matrix = compute_heat_matrix(frame, frames_queue)
      #Get co-ordinate of highest value in heat_matrix
      highest_cord = np.unravel_index(heat_matrix.argmax(), heat_matrix.shape)
      #calculate the vector as (x1-x2),(y1-y2)
      vector = [shape/2,shape/2] - highest_cord
      return vector