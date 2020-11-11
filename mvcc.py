import time
from mvcc_resource import *


# Copied From Execute.py
file = open("data-input-3.txt", "r")
myfile = file.read()
arr = myfile.split("; ")

array_transaksi = []
for data in arr:
    data = str(data)
    jenis = data[0]
    if jenis != "C":
        item = data[-2]
        transaksi = data[1:-3]
    else:
        item = ""
        transaksi = data[1:]

    array_transaksi.append((jenis, transaksi, item))

file.close()

# Let it full of actions, inside action would be (jenis, transaksi, item)
# Action is schedule

actions = array_transaksi

transaction_timestamps = []

start_time = time.time()

for action in actions :
    if not(int(action[1]) in transaction_timestamps):
        transaction_timestamps.append(int(action[1]))
# Sorting the timestamps
transaction_timestamps.sort()


# Create transactions based on timestamps
transactions = []
for i in range(len(transaction_timestamps)) :
    transaction = Transaction(transaction_timestamps[i])
    transactions.append(transaction)

resources = []
max_transaction_timestamp = -1
min_transaction_timestamp = 9999

for action in actions :

    # Add action to its Transaction
    timestamp = int(action[1])

    for i in range(len(transaction_timestamps)) :
        if (timestamp == int(transactions[i].get_timestamp())) :
            transactions[i].add_action(action)
            break

    if (timestamp > max_transaction_timestamp) :
        max_transaction_timestamp = timestamp

    if (timestamp < min_transaction_timestamp) :
        min_transaction_timestamp = timestamp
    
    if (action[2] != "" and not(action[2] in resources)):
        resources.append(action[2])

total_resource = len(resources)

# Matrix for versions of Resources
versions_of_resource = [[None for j in range(min_transaction_timestamp, max_transaction_timestamp + 2)] for i in range (total_resource)]

# Insert All Initial Versions of all resources
for i in range(total_resource) :
    default_resource_ver = Resource(resources[i], i, 0, 0, 0)
    versions_of_resource[i][0] = default_resource_ver


print_actions_in_order(actions)
print()


data = 1 # set data for write action
# Lets evaluate the schedule
commit_waiting_list = []
for action in actions :
    action_type = action[0]
    ts = action[1] # Timestamp of transaction in Action [In Str]
    ts_int = int(ts) # Timestamp of transaction in Action [In Int]
    res_name = action[2]

    

    t_act = get_trasaction_by_ts(transactions, ts_int)
    res_idx = get_resource_col_num(res_name, versions_of_resource)

    if (t_act.get_abort_status() or t_act.get_rollback_status()):
        continue

    # If Read
    if (action_type == "R") :
        qk = get_biggest_wts_res(res_name, ts_int, versions_of_resource)
        qk.read(t_act, versions_of_resource, transactions)

    # If Write
    elif (action_type == "W") :
        # Implement Write here
        qk = get_biggest_wts_res(res_name, ts_int, versions_of_resource)
        data = data + 1
        new_resource = qk.write(data, t_act, versions_of_resource, transactions, actions)

        if (new_resource):
            versions_of_resource[res_idx][ts_int] = new_resource
        

    elif (action_type == "A") : # Action is Abort
        t_act.abort()


    else : # Action type is Commit
        is_commit_success = t_act.commit(transactions)

        if (is_commit_success):
            # check if any trasaction can commit after this trasaction commit
            affected_ts = t_act.get_affects()

            if (len(commit_waiting_list) != 0) and (len(affected_ts) != 0):
                for iter_affected_ts in affected_ts:
                    if (is_available_action_in_array_by_ts(iter_affected_ts, commit_waiting_list)):
                        idx = get_act_idx_in_array_by_ts(iter_affected_ts, commit_waiting_list)
                        pop_act = commit_waiting_list[idx]
                        del commit_waiting_list[idx]
                        act_ts = int(pop_act[1]) # Timestamp of Commit
                        will_be_commited_ts = get_trasaction_by_ts(transactions, act_ts)
                        commit_status = will_be_commited_ts.commit(transactions) 
                        if not(commit_status):
                            commit_waiting_list.append(pop_act)

        else :
            commit_waiting_list.append(action)
    


for trans in transactions:
    if (trans.rollbacks) :
        print("T" + str(trans.timestamp) + " runs serially")
        # Remove Actions whose transaction is rollbacked 
        for action in trans.actions :
            if (int(action[1]) == int(trans.timestamp)):
                actions.remove(action)

        for action in trans.actions :
            actions.append(action)

    

print_actions_in_order(actions)
end_time = time.time()
print("Time Elapsed :", end_time - start_time, "Seconds")