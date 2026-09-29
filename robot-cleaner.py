import copy


#Υπολογιζω το κοστος για να χρησιμοποιησω στη μεθοδο BestFS
def trash_calc(state):
    
    trash_left= sum(state[1:9]) 
    trash_in_robot = state[-1]             
    
    return trash_left + trash_in_robot






#-------------------------------------Τελεστες----------------------------------

def move_left(state):
    
    
    #Ελεγχω αμα εχω χωρο στα αριστερά για κα κουνηθει η σκούπα
    if state[0] > 1:
        #Μετακινω στην σκουπα αριστερά
        state[0] = state[0] - 1  
        
        #Ελεγχω αν η σκουπα εχει χωρο για σκουπίδια.
        if state[-1] < 3: 
            #Ελεγχω αν η σκουπα εχει χωρο για μερικα σκουπίδια
            #που ειναι στο πλακάκι
            if state[state[0]] > 3 - state[-1]:
                state[state[0]] = state[state[0]] - (3 - state[-1])
                state[-1] = 3
            ##Ελεγχω αν η σκουπα εχει χωρο για ολα τα σκουπίδια
            #που ειναι στο πλακακι
            else:
                state[-1] = state[-1] + state[state[0]]
                state[state[0]] = 0
        
        return state
    else:
        return None 
    
    
		
def move_right(state):
    #Ελεγχω αμα εχω χωρο στα αριστερά για κα κουνηθει η σκούπα
    if state[0] < 8:
        #Μετακινω στην σκουπα δεξια
        state[0] = state[0] + 1  

        #Ελεγχω αν η σκουπα εχει χωρο για σκουπίδια.
        if state[-1] < 3: 
            #Ελεγχω αν η σκουπα εχει χωρο για μερικα σκουπίδια
            #που ειναι στο πλακάκι
            if state[state[0]] > 3 - state[-1]:
                state[state[0]] = state[state[0]] - (3 - state[-1])
                state[-1] = 3
            #Ελεγχω αν η σκουπα εχει χωρο για ολα τα σκουπίδια
            #που ειναι στο πλακακι
            else:
                state[-1] = state[-1] + state[state[0]]
                state[state[0]] = 0
                
        return state
    else:
        return None
          
          
          
       
def full(state):
    
    # Υπολόγιζω ποσα σκουπίδια έχουνν μεινει στο πάτωμα.
    trash_left = sum(state[1:9])
    
    full_robot = (state[-1] == 3)
    
    #Συνθηκη οπου δεν εχει μεινει τιποτα στο πατωμα αλλα υπαρχουν 
    #σκουπιδια στην σκουπα. Θα χρησιμοποιηθει στο τελος του προγραμματος
    #ωστε να μπορεσει να αδειασει η σκουπα χωρις να ειναι γεματη και να 
    #εχει την δυνατοτητα να τερματησει το προγραμματα.
    endgame = (trash_left == 0 and state[-1] > 0 )
    
    
   # Έλεγχω αν η σκουπα είναι στη βαση και ειτε ειναι γεματη ειτε τηρει
   #την τελευταια συνθηκη (endgame)
    if state[0] == state[9] and (full_robot or endgame):
        state[-1] = 0  
        return state
        
    return None
        
        
        
        
#---------------------------------Παιδια------------------------------------
        
def find_children(state):
    children = []
    
    #Κανω αντίγραφο και δοκιμαζω την αριστερη κινηση
    left_state = copy.deepcopy(state)
    left_child = move_left(left_state)
    if left_child != None: 
        children.append(left_child)
        
    #Κανω αντιγραφο και δοκιμαζω την δεξιά κινηση
    right_state = copy.deepcopy(state)
    right_child = move_right(right_state)
    if right_child != None: 
        children.append(right_child)
    
    #Κανω αντιγραφο και δοκιμαζω να αδειασει την σκουπα
    full_state = copy.deepcopy(state)
    full_child = full(full_state)
    if full_child != None:
        children.append(full_child)
        
    return children
    
    
#-------------------------------Front & Queue---------------------------------
    
def make_front(state):
    #Μετατρέπω την κατασταση σε λιστα
    return [state]

def make_queue(state):
    #Αρχικοποιω την ουρα ιστορικου με το αρχικο μονοπάτι
    return [[state]]
    
    
    
    
def expand_front(front, method):  
    if front:
        
        '''
        ---------------------------------------------------
        Πρωην κωδικας (για ελεγχο) που γεμιζε το terminal.
        ---------------------------------------------------
        print("Current Front : \n")
        print(front) 
        '''
        
        # Αν η μεθοδος είναι DFS:
        if method == 'DFS':    
            node = front.pop(0) 
            
            for child in find_children(node): 
                #Βαζω τα παιδιά στην αρχή της λίστας γιατι η DFS ειναι LIFO
                front.insert(0, child) 
                
        # Αν η μεθοδος είναι BFS:
        elif method == 'BFS':
            node = front.pop(0) 
            for child in find_children(node):
                #Βαζω τα παιδιά στο τελος της λίστας γιατι η DFS ειναι FIFO
                front.append(child)
                
                # Αν η μεθοδος είναι BestFS:
        elif method == 'BestFS':
            front.sort(key=trash_calc)
            node = front.pop(0) 
            for child in find_children(node):
                #Δεν εχει σημασια που βαζω τα παιδιά στην λίστα 
                #γιατι θα γινει sort ετσι και αλλιως
                front.append(child)
                
        
                
    return front
    
    
    
    
def extend_queue(queue, method):
    
    if queue:
        
        
        node = queue.pop(0) 
        children = find_children(node[-1]) 
        
       #Κανω expand την ουρά ανάλογα με τη μέθοδο ωστε να ειναι σωστα
       #συγχρονισμενη με το πραγματικο μονοπατι
        if method == 'DFS':
            for child in children:
                path = copy.deepcopy(node)
                path.append(child) 
                #Για BFS κσι BestFS, έβαλα το νεο μονοπατι στο τέλος.
                queue.insert(0, path) 
        
        
        elif method == 'BFS' or method == 'BestFS':
            for child in children:
                path = copy.deepcopy(node)
                path.append(child)
                #Για BFS κσι BestFS, έβαλα το νεο μονοπατι στο τέλος.
                queue.append(path) 
    
    return queue    
    
    
    
    
    
    
    
    
    
    
    
    
#-------------------------------Επιλυση----------------------------------------
    
def find_solution(front, queue, closed, goal, method):

       
    if not front:
        print('No Solution Available \n')
    
    #Ελεγχω άμα εχω ξαναεξετασει αυτη την κατασταση
    elif front[0] in closed:
        new_front=copy.deepcopy(front)
        #Αφαιρω την κατάσταση
        new_front.pop(0)
        new_queue=copy.deepcopy(queue)
        #Αφαιρω το αντιστοιχο μονοπατι
        new_queue.pop(0)
        #Καλω αναδρομικα την συναρτηση με το νεο front
        find_solution(new_front, new_queue, closed, goal, method)
      
    
    #Ελεγχω άμα εχω φτασει στην κατασταση-στοχο.
    elif front[0]==goal:
        print('Solution Found! Here is the path : ')
        path_solution=queue[0]
        print(path_solution)
        
        path_length=len(path_solution)-1
        print("\nStatistics :\n")
        print("Steps to Goal (Path Length): ", path_length) 
        
        
        states_length=len(closed)
        print("Total States Visited (Search Effort):", states_length)
       
        
        
    else:
        #Προσθετω την τρεχουσα κατάσταση στη λιστα των καταστασεων
        #που εχω επισκεφτει
        closed.append(front[0])
        front_copy=copy.deepcopy(front)
        front_children=expand_front(front_copy, method)
        queue_copy=copy.deepcopy(queue)
        queue_children=extend_queue(queue_copy, method)
        closed_copy=copy.deepcopy(closed)
        #Συνεχιζω την αναζητηση αναδρομικα
        find_solution(front_children, queue_children, closed_copy, goal, method)
        
        


#-------------------------------Main-------------------------------------------



def main():
    
    initial_state = [3, 2, 3, 0, 0, 2,0,1,8,3,0] 
    goal = [3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]
    
   #Εφτιαξα το μενου επιλογής μεθόδου οπως ζητειται στο ερωτημα 7
    while True:
        print("Pick a method: \nPress 1 for DFS \nPress 2 for BFS \nPress 3 for BestFS")
        meth = input()
        if meth =='1':
            method = 'DFS'
            break
        elif meth =='2':
            method = 'BFS'
            break
        elif meth =='3':
            method = 'BestFS'
            break
        else:
            print("The only choices are 1, 2 and 3, try again")
                
    print(f"You picked the method {method}")
    
    
    #Εφτιαξα το μενου επιλογής καταστασης οπως ζητειται στο ερωτημα 8
    while True:
        print("Pick an Initial State: \nPress 1 for default Initial State : [3, 2, 3, 0, 0, 2,0,1,8,3,0] \nPress 2 for Initial State : [4, 2, 3, 0, 0, 2,0,1,8,3,0]  \nPress 3 for Initial State : [6, 2, 3, 0, 0, 2,0,1,8,3,0]")
        in_state = input()
        if in_state =='1':
            break
        elif in_state =='2':
            initial_state = [4, 2, 3, 0, 0, 2,0,1,8,3,0]
            break
        elif in_state =='3':
            initial_state = [6, 2, 3, 0, 0, 2,0,1,8,3,0]
            break
        else:
            print("The only choices are 1, 2 and 3, try again")
                
    print(f"You picked the Initial State : {initial_state}")
    
    
    
    
    
    
  
    print('Initiating Search')
    find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)
    
if __name__ == "__main__":
    main()
