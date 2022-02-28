# Python3 program to construct tree using  
# inorder and postorder traversals  
  
# Helper function that allocates  
# a new node  
class newNode: 
    def __init__(self, data): 
        self.data = data  
        self.left = self.right = None
  
# Recursive function to construct binary  
# of size n from Inorder traversal in[]  
# and Postorder traversal post[]. Initial  
# values of inStrt and inEnd should be  
# 0 and n -1. The function doesn't do any  
# error checking for cases where inorder  
# and postorder do not form a tree  
def buildUtil(In, post, inStrt, inEnd, pIndex): 
      
    # Base case  
    if (inStrt > inEnd):  
        return None
  
    # Pick current node from Postorder traversal  
    # using postIndex and decrement postIndex  
    node = newNode(post[pIndex[0]])  
    pIndex[0] -= 1
  
    # If this node has no children  
    # then return  
    if (inStrt == inEnd):  
        return node  
  
    # Else find the index of this node  
    # in Inorder traversal  
    iIndex = search(In, inStrt, inEnd, node.data)  
  
    # Using index in Inorder traversal,  
    # construct left and right subtress  
    node.right = buildUtil(In, post, iIndex + 1,  
                                  inEnd, pIndex)  
    node.left = buildUtil(In, post, inStrt,  
                        iIndex - 1, pIndex)  
  
    return node 
  
# This function mainly initializes index  
# of root and calls buildUtil()  
def buildTree(In, post, n): 
    pIndex = [n - 1]  
    return buildUtil(In, post, 0, n - 1, pIndex) 
  
# Function to find index of value in  
# arr[start...end]. The function assumes  
# that value is postsent in in[]  
def search(arr, strt, end, value): 
    i = 0
    for i in range(strt, end + 1): 
        if (arr[i] == value):  
            break
    return i 
  
# This funtcion is here just to test  
def preOrder(node): 
    if node == None:  
        return
    print(node.data, end=", ") 
    preOrder(node.left)  
    preOrder(node.right) 
  

inOrder = [9, 11, 33, 35, 38, 40, 44, 48, 61, 85, 89, 101, 106, 110, 135, 150, 159, 180, 188, 200, 201, 214, 241, 253, 268, 269, 275, 278, 285, 301, 301, 327, 356, 358, 363, 381, 396, 399, 413, 428, 434, 445, 449, 462, 471, 476, 481, 492, 496, 497, 509, 520, 526, 534, 540, 589, 599, 613, 621, 621, 623, 628, 634, 650, 652, 653, 658, 665, 679, 691, 708, 711, 716, 722, 752, 756, 764, 771, 773, 786, 807, 808, 826, 827, 836, 842, 856, 867, 875, 877, 879, 889, 892, 922, 946, 951, 965, 980, 993, 996]
postOrder = [35, 33, 44, 40, 38, 48, 11, 85, 89, 61, 110, 150, 159, 135, 188, 200, 180, 106, 101, 214, 268, 275, 269, 253, 241, 201, 9, 301, 301, 285, 327, 356, 363, 396, 413, 399, 445, 434, 462, 449, 428, 471, 481, 492, 496, 497, 476, 381, 358, 278, 534, 526, 520, 613, 599, 623, 621, 621, 589, 540, 628, 650, 653, 652, 665, 691, 679, 711, 756, 752, 722, 716, 807, 786, 773, 771, 826, 808, 827, 764, 856, 875, 867, 842, 836, 708, 879, 892, 889, 922, 877, 951, 946, 658, 980, 996, 993, 965, 634, 509]
n = len(inOrder)
root = buildTree(inOrder, postOrder, n)
print("ISITDTU{", end="")
preOrder(root)
