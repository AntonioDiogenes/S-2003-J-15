class Node:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        self.left = None
        self.right = None

class BinaryTree:
    
    def __init__(self):
        self.root = None

    def insert(self, value1, value2):
        new_node = Node(value1, value2)
        
        if self.root is None:
            self.root = new_node
            return
        
        current_node = self.root
        
        while True:
            if value1 == current_node.value1 and value2 == current_node.value2:
                return
            elif value1 < current_node.value1 or (value1 == current_node.value1 and value2 < current_node.value2):
                if current_node.left is None:
                    current_node.left = new_node
                    return
                else:
                    current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = new_node
                    return
                else:
                    current_node = current_node.right

    def delete(self, value1, value2):
        node = self.root
        parent_node = None
        is_left_child = True
        
        while node:
            if node.value1 == value1 and node.value2 == value2:
                if not node.left and not node.right:
                    if not parent_node:
                        self.root = None
                    elif is_left_child:
                        parent_node.left = None
                    else:
                        parent_node.right = None
                elif not node.left:
                    if not parent_node:
                        self.root = node.right
                    elif is_left_child:
                        parent_node.left = node.right
                    else:
                        parent_node.right = node.right
                elif not node.right:
                    if not parent_node:
                        self.root = node.left
                    elif is_left_child:
                        parent_node.left = node.left
                    else:
                        parent_node.right = node.left
                else:
                    successor = self._find_successor(node)
                    if not parent_node:
                        self.root = successor
                    elif is_left_child:
                        parent_node.left = successor
                    else:
                        parent_node.right = successor
                    successor.left = node.left
                    
                return True
            elif value1 < node.value1 or (value1 == node.value1 and value2 < node.value2):
                parent_node = node
                node = node.left
                is_left_child = True
            else:
                parent_node = node
                node = node.right
                is_left_child = False
                
        return False

    def _find_successor(self, node):
        parent_successor = node
        successor = node
        current = node.right
        
        while current:
            parent_successor = successor
            successor = current
            current = current.left
        
        if successor != node.right:
            parent_successor.left = successor.right
            successor.right = node.right
        
        return successor

    def traverse(self):
        self._traverse_in_order(self.root)

    def _traverse_in_order(self, node):
        if node:
            self._traverse_in_order(node.left)
            array = [f"({node.value1}, {node.value2})"]
            
            self._traverse_in_order(node.right)
    
    def search(self, value1, value2=None):
            node = self.root

            while node:
                if node.value1 == value1 and (value2 is None or node.value2 == value2):
                    return node
                elif value1 < node.value1 or (value1 == node.value1 and (value2 is None or value2 < node.value2)):
                    node = node.left
                else:
                    node = node.right

            return None

"""tree = BinaryTree()
tree.insert(5, "cinco")
tree.insert(3, "três")
tree.insert(2, "dois")
tree.insert(8, "oito")
tree.insert(7, "sete")
tree.insert(10, "dez")

# buscar pelo nó com valor (7, "sete")
node = tree.search(10)
print(node.value1, node.value2) # saída: 7 sete"""