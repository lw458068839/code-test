import psycopg2


def get_last_son(result_dict):
    key_list = list(result_dict.keys())[:]
    father_set = set()
    for key in key_list:
        father_set.add(result_dict[key]['father'])
    for key in key_list:
        if key in father_set:
            pass
        else:
            res = result_dict.pop(key)
            result_dict[res['father']]['sons'].append(res)
            get_last_son(result_dict)
    for k,v in result_dict.items():
        if v['father']!=None:
            continue
    result = {'name': 'todo', 'done': False, 'nid': None, 'father': None, 'sons': []}
    for k, v in result_dict.items():
        result['sons'].append(v)
    return result






class DataBaseConnection:
    def __init__(self,database="database",user="root",password="123456",host="127.0.0.1",port="5432"):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def update_query(self,query,*data):
        cur = self.conn.cursor()
        state = 0
        ret = None
        try:
            cur.execute(query,data)
            self.conn.commit()
            state = 1
        except Exception:
            self.conn.rollback()
        return state,ret

    def select_query(self,query,*data):
        cur = self.conn.cursor()
        state = 0
        ret = None
        try:
            state = 1
            cur.execute(query, data)
            ret = cur.fetchall()
        except Exception:
            pass
        return state,ret

    def data_pause(self):
        query = 'SELECT id,name,done,father_id FROM task'
        state, ret = self.select_query(query)
        result_dict = {}
        key_set = set()  # 存放所有id
        if state:
            for task in ret:
                result_dict[task[0]] = {
                    "name": task[1],
                    "nid": task[0],
                    "done": task[2],
                    "father": task[3],
                    "sons": []
                }
                key_set.add(task[0])
        level_list = [[None, ]]
        while len(key_set) != 0:
            my_set = set()
            for key in key_set:
                father_id = result_dict[key]['father']
                if father_id in level_list[-1]:
                    my_set.add(key)
            key_set = key_set - my_set
            level_list.append(my_set)
        for keys in level_list[:1:-1]:
            for key in keys:
                res = result_dict.pop(key)
                result_dict[res['father']]['sons'].append(res)
        task_dict = {"todo": [], "complate": []}
        for v in result_dict.values():
            if v['done'] == True:
                task_dict['complate'].append(v)
            else:
                task_dict['todo'].append(v)
        return task_dict

my_conn = DataBaseConnection()



if __name__=='__main__':
    query = 'SELECT id,name,done,father_id FROM task'
    state,ret = my_conn.select_query(query)
    result_dict = {}
    key_set = set()              # 存放所有id
    if state:
        for task in ret:
            result_dict[task[0]]={
                "name":task[1],
                "nid":task[0],
                "done":task[2],
                "father":task[3],
                "sons":[]
            }
            key_set.add(task[0])
    level_list =[[None,]]
    while len(key_set)!=0:
        my_set=set()
        for key in key_set:
            father_id = result_dict[key]['father']
            if father_id in level_list[-1]:
                my_set.add(key)
        key_set = key_set-my_set
        level_list.append(my_set)
    for keys in level_list[:1:-1]:
        for key in keys:
            res = result_dict.pop(key)
            result_dict[res['father']]['sons'].append(res)
    task_dict = {"todo":[],"complate":[]}
    for v in result_dict.values():
        if v['done']==True:
            task_dict['complate'].append(v)
        else:
            task_dict['todo'].append(v)
    print(task_dict)






