
from numpy import dot
from numpy.linalg import norm
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
    score = 0

    #TODO:
    #Judge how well we sing
    #ref_list, inf_list

    score = dot(ref_list, inf_list)/(norm(ref_list)*norm(inf_list))
        
    return score