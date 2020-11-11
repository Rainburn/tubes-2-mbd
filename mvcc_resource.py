class Transaction :

    def __init__(self, ts):
        self.timestamp = ts
        self.actions = []
        self.affects = []
        self.commit_status = False
        self.aborted = False
        self.rollbacks = False

        # Let the cascade : T1 -> T2 -> T3
        # T1.affects = [T2]
        # T2.affects = [T3]

    def get_timestamp(self):
        return int(self.timestamp)
    
    def get_actions(self):
        return self.actions
    
    def get_commit_status(self):
        return self.commit_status
    
    def get_affects(self):
        return self.affects
    
    def get_rollback_status(self) :
        return self.rollbacks

    def commit(self, transactions):
        affecting = self.get_affecting_ts(transactions)
        all_commit = True
        failing_ts = []

        if (affecting != None) :
            for ts in affecting :

                if (ts.get_commit_status() == False):
                    all_commit = False
                    failing_ts.append(ts)
                    break

        if (all_commit) :
            print("Commit of T" + str(self.timestamp) + " Success")
            self.commit_status = True
            return True

        else :
            print("Commit of T" + str(self.timestamp) + " Fails because T" + str(failing_ts[0].get_timestamp()) + " has not commited yet.")
            return False

    def add_action(self, action):
        self.actions.append(action)

    def __str__(self):
        return "T" + str(self.timestamp)

    def change_timestamp(self, ts) :
        self.timestamp = ts
        for i in range(len(self.actions)):
            self.actions[i][1] = ts

    def add_affect(self, transaction):
        self.affects.append(transaction)
    
    def pop_affect(self):
        return self.affects.pop()
    
    def get_abort_status(self):
        return self.aborted

    def abort(self, matrix, transactions, actions):
        self.aborted = True
        print("T" + str(self.timestamp) + " aborts")

        for i in range(len(matrix)):
            ts_int = int(self.timestamp)
            matrix[i][ts_int] = None

        # Cascading Rollback
        if (len(self.affects) > 0):
            for t in self.affects :
                    print("Cascading from T" + str(self.timestamp) + " -> ", end = "")
                    t.rollback(matrix, transactions, actions)



    def get_affecting_ts(self, transactions) :
        affecting = []
        for ts in transactions:
            affected_ts = ts.get_affects()
            if (len(affected_ts) == 0):
                continue
            else :
                for t in affected_ts:
                    if (t.get_timestamp() == self.timestamp):
                        affecting.append(ts)
                        break
        
        return affecting

    def rollback(self, matrix, transactions, actions): # With Cascading  

        self.rollbacks = True  

        if not(self.aborted):
            print("T" + str(self.timestamp) + " rollbacks")
            print()

        for i in range(len(matrix)):
            ts_int = int(self.timestamp)
            matrix[i][ts_int] = None

        # Cascading Rollback
        if (len(self.affects) > 0):
            for t in self.affects :
                    print("Cascading from T" + str(self.timestamp) + " -> ", end = "")
                    t.rollback(matrix, transactions, actions)

class Resource :
    
    def __init__(self, name, val, ver, rts, wts):
        self.name = name
        self.version = ver
        self.rts = rts
        self.wts = wts
        self.value = val

        self.print_stats()

    def __str__(self):
        return self.name + self.version
    
    def read(self, transaction, matrix, transactions) :

        tts = int(transaction.get_timestamp())

        if (tts < self.wts) :
            # Find older version
            older_ver = retrieve_older_version(self, matrix)
            older_ver.read(transaction, matrix)

        else :
            
            print("T" + str(tts) + " performs a read of " + self.name + ", it's going to read " + self.name + str(self.version))
    
            if (self.version != tts) and (self.version != 0):
                add_cascade(self.version, tts, transactions)

            self.rts = max(self.rts, tts)

            self.print_stats()

            return self.value

            

    def write(self, data, transaction, matrix, transactions, actions) :
        
        tts = int(transaction.get_timestamp())

        if (tts < self.rts) :
            # Rollback
            print("T" + str(tts) + " performs Write on " + self.name + ", but " + self.name + str(self.version) + " has been read by transaction T" + str(self.rts))
            transaction.rollback(matrix, transactions, actions)
            return False
            
        # Update data
        elif (tts == self.wts) :
            print("T" + str(tts) + " performs Write on " + self.name + ", it updates the value of " + self.name + str(self.version))
            self.value = data
            self.print_stats()
        
        # create new version
        else :
            print("T" + str(tts) + " performs Write on " + self.name + ", it creates new version " + self.name + str(tts))
            new_version = tts
            new_resource = Resource(self.name, data, new_version, tts, tts)
            return new_resource

    # Getter  
    def get_name(self):
        return self.name

    
    def get_value(self):
        return self.value
    

    def get_version(self):
        return self.version
    
    def get_rts(self):
        return self.rts

    def get_wts(self):
        return self.wts

    # Setter
    
    def set_value(self, val):
        self.value = val
    

    def set_rts(self, rts) :
        self.rts = rts
    
    def set_wts(self, wts) :
        self.wts = wts

    def print_stats(self) :
        print("RTS(" + self.name + str(self.version) + ") : " + str(self.rts), end = " | ")
        print("WTS(" + self.name + str(self.version) + ") : " + str(self.wts))
        print()

def get_resource_col_num(res_name, matrix):
    idx = -1
    for i in range(len(matrix)):
        if (res_name == matrix[i][0].get_name()):
            idx = i
            break

    return idx


def get_resource_by_ver(res_name, ver_num, matrix):
    col_idx = get_resource_col_num(res_name, matrix)
    for i in range(len(matrix[col_idx])):

        if (matrix[col_idx][i] == None):
            continue

        if (matrix[col_idx][i].get_version() == ver_num):
            return matrix[col_idx][i]
    
    return None



def get_most_recent_resource(res_name, matrix):
    idx = get_resource_col_num(res_name, matrix)
    for i in range(len(matrix[idx]) - 1, -1, -1):
        if (matrix[idx][i] != None):
            return matrix[idx][i]

def retrieve_older_version(res, matrix):
    res_name = res.get_name()
    total_resource = len(matrix)

    res_idx_in_matrix = 0
    for i in range(total_resource) :
        if (matrix[i][0].get_name() == res_name) :
            res_idx_in_matrix = i
            break

    res_ver = res.get_version()
    older_res_ver = res_ver - 1
    while (older_res_ver >= 0) :
        if (matrix[res_idx_in_matrix][older_res_ver] == None) :
            older_res_ver = older_res_ver - 1
            continue
        else :
            return matrix[res_idx_in_matrix][older_res_ver]
    
    if (older_res_ver == -1) :
        return None


def get_biggest_wts_res(res_name, tts, matrix):
    ver = 0
    max_wts = 0
    col_idx = get_resource_col_num(res_name, matrix)
    # Convert tts to int
    tts_int = int(tts)

    for i in range(len(matrix[col_idx])):

        if (matrix[col_idx][i] == None) :
            continue

        if (matrix[col_idx][i].get_wts() > max_wts) and (matrix[col_idx][i].get_wts() <= tts_int):
            max_wts = matrix[col_idx][i].get_wts()
            ver = matrix[col_idx][i].get_version()

    return get_resource_by_ver(res_name, ver, matrix)



def add_matrix_row(matrix, rows = 1) :
    cols = len(matrix)
    for i in range(cols):
        for j in range(rows):
            matrix[i].append(None)

def get_trasaction_by_ts(transactions, ts):
    for t in transactions:
        if (ts == t.get_timestamp()):
            return t

    return None

def add_cascade(affecting_trans, affected_trans, transactions) :
    affecting_trans = int(affecting_trans)
    affected_trans = int(affected_trans)
    for t in transactions :
        if (affecting_trans == t.get_timestamp()) :
            for t_affected in transactions :
                if (affected_trans == t_affected.get_timestamp()):
                    t.add_affect(t_affected)

def is_available_action_in_array_by_ts(transaction, array):
    
    if (len(array) == 0):
        return False

    for act in array :
        if (int(transaction.get_timestamp()) == int(act[1])) :
            return True

    return False

def get_act_idx_in_array_by_ts(transaction, array):

    if (len(array) == 0) :
        return -999

    for i in range(len(array)):
        if (int(transaction.get_timestamp()) == int(array[i][1])) :
            return i

    return -999 # Not Found

def print_actions_in_order(actions) :
    for action in actions :
        if (action[0] == "C") :
            print(action[0] + str(action[1]), end = " ")
        
        else :
            print(action[0] + str(action[1]) + "(" + action[2] + ")", end = " ")
    
    print()

def actions_in_order(actions) :

    order = ""

    for action in actions :
        if (action[0] == "C") :
            order = order + action[0] + str(action[1]) + "; "
        
        else :
            order = order + action[0] + str(action[1]) + "(" + action[2] + "); "
    
    return order

