import tornado.ioloop
import tornado.web
import tornado.template
from conn_db import my_conn
import json

def update_done(nid):
    query_father = "select father_id,name from task where id=%d"%nid
    state,ret = my_conn.select_query(query_father)
    father_id = ret[0][0]
    if father_id==None:
        return
    son_id = "select id,done,name from task where father_id=%s"%father_id
    state, ret = my_conn.select_query(son_id)
    for item in ret:
        if item[1]==False:
            return
    update_query = "UPDATE task set done=%s where id=%s"
    my_conn.update_query(update_query,True,father_id)
    update_done(father_id)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('template/index.html')

class TaskHandler(tornado.web.RequestHandler):
    def get(self):
        data = my_conn.data_pause()
        self.finish(data)

    def post(self):
        update_data = json.loads(self.request.body.decode('utf-8'))
        nid = update_data.get('nid',None)
        if nid is not None:
            # update task
            data = update_data.get('newData')
            set_data=''
            data_list = []
            for k,v in data.items():
                data_list.append(v)
                if set_data=='':
                    set_data+='%s'%k+'=%s'
                else:
                    set_data+=',%s'%k+'=%s'
            update_query="UPDATE task set "+set_data+" where id=%s"
            data_list.append(nid)
        else:
            # insert task
            data = update_data.get('newData')
            data['father_id'] = update_data.get('father_id')
            data['done']=False
            keys = ''
            valus = ''
            data_list = []
            for k, v in data.items():
                data_list.append(v)
                if keys == '':
                    keys += '%s'%k
                    valus += '%s'
                else:
                    keys += ',%s' % k
                    valus += ',%s'
            update_query = "INSERT into task ("+keys+") values ("+valus+")"
        my_conn.update_query(update_query,*data_list)
        if data.get('done', None) == True:
            update_done(nid)
        data = my_conn.data_pause()
        self.finish(data)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/v1/task", TaskHandler),
    ],
        static_path='static',
        autoescape=None,
        autoreload=True
    )

if __name__ == "__main__":
    app = make_app()  # 创建一个应用对象
    app.listen(8888)  # 设置端口
    tornado.ioloop.IOLoop.current().start()
