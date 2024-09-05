
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from ..log.logger._loguru import LoguruHandler

logger = LoguruHandler()

class DBManager:
    # # 测试封装类的方法(推荐是使用ORM的方法来操作映射类而不是SQL语句)

    # # 创建封装类的实例
    # db_manager = DBManager()

    # # 执行建表语句
    # db_manager.execute('create table if not EXISTS user (id int PRIMARY KEY auto_increment,name char (32), age int);')

    # # 执行插入语句
    # insert_query = "INSERT INTO users (name, age) VALUES (:name, :age)"
    # db_manager.execute((insert_query, {'name': 'Alice', 'age': 30})

    # # 执行查询语句
    # result = db_manager.execute('select * from user;')
    # print(result.fetchall())

    # # 执行删除语句
    # db_manager.execute('delete from user where id = 1;')

    # # 执行删表语句
    # delete_query = "DELETE FROM users WHERE name = :name"
    # db_manager.execute(delete_query, {'name': 'Alice'})
    def __init__(self, db_url):
        # 创建会话类
        # db_url = 'mysql+pymysql://root:123456@localhost:3306/test?charset=utf8'
        engine = create_engine(db_url)
        # 创建连接引擎
        self.Session = sessionmaker(bind=engine)
    
    def execute(self, sql, params=None):
        # 执行SQL语句
        try:
            # 创建会话对象
            with self.Session() as session:
                if params:
                    # 执行SQL语句
                    result = session.execute(sql, params)
                else:
                    result = session.execute(sql)
                session.commit() # 提交事务
                return result
        except SQLAlchemyError as e:
            session.rollback()
            logger.warning(f"An error occurred: {e}")
            return None


# 定义ORM的类

# 创建基类, # 所有的模型类都继承自此类
Base = declarative_base()

class ORMManager:
    # # 测试ORM的类的方法

    # # 定义映射类
    # from sqlalchemy import create_engine, Column, Integer, String
    #
    # class User(Base):
    #     __tablename__ = 'user' # 表名
    #     id = Column(Integer, primary_key=True) # 主键
    #     name = Column(String(20)) # 姓名
    #     age = Column(Integer) # 年龄

    # # 创建ORM的类的实例
    # orm_manager = ORMManager()

    # # 添加用户Alice，年龄18岁
    # user1 = User(name='Alice', age=18) # 创建对象
    # orm_manager.add(user1) # 添加对象

    # # 查询用户Alice的信息
    # result = orm_manager.query(User, name='Alice') # 查询对象列表
    # for user in result:
    #     print(user.name, user.age) # 打印属性

    # # 修改用户Alice的年龄为19岁
    # orm_manager.update(User, condition={'name': 'Alice'}, age=19) # 更新对象

    # # 删除用户Alice的信息
    # orm_manager.delete(User, name='Alice') # 删除对象

    def __init__(self, db_url):
        # 创建会话类
        # 创建连接引擎
        # db_url = 'mysql+pymysql://root:123456@localhost:3306/test?charset=utf8'
        self.engine = create_engine(db_url)
        # 自动创建所有继承自 Base 的表
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables in the database. This should be called manually if needed."""
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session rollback because of exception: {e}")
            raise
        finally:
            session.close()

    def add(self, obj):
        # 添加对象
        # 创建会话对象
        with self.session_scope() as session:
            session.add(obj)
            logger.info("Added object: %s", obj)
    
    def query(self, cls, **kwargs):
        # 查询对象
        with self.session_scope() as session:
            result = session.query(cls).filter_by(**kwargs).all()
            logger.info("Queried objects: %s", result)
            return result
    
    def update(self, cls, condition, **kwargs):
        # 更新对象
        with self.session_scope() as session:
            obj = session.query(cls).filter_by(**condition).first()
            if obj:
                for key, value in kwargs.items():
                    setattr(obj, key, value)
                logger.info("Updated object: %s", obj)
            else:
                logger.warning("No such object found for update")

    def delete(self, cls, **kwargs):
        # 删除对象
        with self.session_scope() as session:
            obj = session.query(cls).filter_by(**kwargs).first()
            if obj:
                session.delete(obj)
                logger.info("Deleted object: %s", obj)
            else:
                logger.warning("No such object found for deletion")
