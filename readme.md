已完成内容：
    - View
        - View tasks
        - View sub-tasks
    - Add
        - Add a task
        - Add a sub-task to a task or sub-task
    - Edit
        - Edit description for task or sub-task
        - Complete a task or sub-task
        - When all sub-tasks are completed, the parent task will be completed as well
    - For backend endpoints
        - Write RESTful endpoints using Python with [Tornado]
    - Save data to PostgreSQL database
未完成内容：
    - (Optional requirement) Due dates
        - Can set a due date when task is created
        - When due date is reached, task will be marked as overdue
    - Secure backend endpoints with OAuth2
    - Write unit tests and integration tests
    - Dockerize application
  
前端实现方式:
    vue+jquery+bootstrap

后端实现方式:
    tornado+psycopg2
    
数据库数据结构:
    表名:task
        字段:
            id:主键,int
            name:task名称,string
            done:完成状态,bool
            create_date:创建时间,date
            father_id:int

部署方法:
    1.数据库
        修改./dockerfile文件下的docker-compose.yml文件,
        将'E:\PyProject\code_test\data'中'E:\PyProject'修改为'code_test'所在路径,
        通过docker-compose up运行
    2.服务器
        python环境3.8.4
        所需包:
            tornado
            psycopg2
        python main.py 运行, 端口8888
    
    


