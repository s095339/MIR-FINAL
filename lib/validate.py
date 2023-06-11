
import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
import math
def validate(ref_list, inf_list):
    """
    Parameter
    ---------------------
    ref_list: pitch list generate from original song
    inf_listL pitch list generate from our sining

    Return
    ---------------------
    The score of our sining
    """

    
    print("--------------")
    score = 0
    print(len(ref_list))
    #TODO:
    length = min(len(ref_list), len(inf_list))
   
    ref_list_sampled = np.array([np.mean(ref_list[idx:idx+14]) for idx in range(0,length-15,15)])
    inf_list_sampled = np.array([np.mean(inf_list[idx:idx+14]) for idx in range(0,length-15,15)])
    
    plt.subplot(2,1,1)
    plt.plot(ref_list_sampled)
    plt.title("ref song")
    plt.subplot(2,1,2)
    plt.plot(inf_list_sampled)
    plt.title("recorded song")
    plt.show()
    print(len(ref_list_sampled))
    score = dot(ref_list_sampled, inf_list_sampled)/(norm(ref_list_sampled)*norm(inf_list_sampled))*100
    
    #for idx in range(length):
        
    
    return score
