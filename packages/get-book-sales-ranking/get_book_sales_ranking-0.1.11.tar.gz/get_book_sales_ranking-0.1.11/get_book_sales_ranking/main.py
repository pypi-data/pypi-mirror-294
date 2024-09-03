# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from quart import Quart, request, abort, jsonify
# from quart_rate_limiter import rate_limit
# from sqlalchemy import Column, Integer, String, select
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import declarative_base, sessionmaker
# # from dotenv import load_dotenv
# import hmac
# import hashlib
# import base64
# import time
# import os
# from datetime import timedelta, datetime
# from ipaddress import ip_address, ip_network
# from contextlib import asynccontextmanager

# from get_book_sales_ranking.data_fix.clean_up import merge_data

# # app = Flask('app')
# app = Quart(__name__)

# @app.route('/')
# def hello_world():
#   return 'Hello, World!'

# # 確認用17:30 問題無し
# @app.route("/google")
# # @rate_limit(5, timedelta(minutes=1))
# async def google():
#     new_data = await get_book_data_google("9784022650597")
#     # new_data = await merge_data()
#     return jsonify(new_data)

# @app.route("/opendb")
# async def opendb():
#     new_data = await get_book_data_opendb("9784022650597")
#     return jsonify(new_data)

# @app.route("/opensearch")
# async def opensearch():
#     new_data = await get_book_data_opensearch("9784022650597")
#     return jsonify(new_data)

# @app.route("/sru")
# async def sru():
#     new_data = await get_book_data_sru("9784022650597")
#     return jsonify(new_data)

# @app.route("/jikkou")
# async def matome():
#     new_data = await jikkou("9784022650597")
#     return jsonify(new_data)

# @app.route("/rakuten")
# async def rakuten():
#     new_data = await fetch_rakuten("9784022650597")
#     return jsonify(new_data)


# @app.route("/bookoff")
# async def bookoff():
#     new_data = await bookoff_main()
#     return jsonify(new_data)

# @app.route("/booklog")
# async def booklog():
#     new_data = await booklog_main()
#     return jsonify(new_data)

# @app.route("/bookmeter")
# async def bookmeter():
#     new_data = await bookmeter_main()
#     return jsonify(new_data)

# @app.route("/clear_up")
# async def clear_up():
#     new_data = await merge_data()
#     return jsonify(new_data)






# # 本番用
# DATABASE_URL = os.environ.get("DATABASE_URL")
# print("DATABASE_URL",DATABASE_URL)

# engine = create_async_engine(DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()

# class Data2(Base):
#     __tablename__ = 'data2'
#     id = Column(Integer, primary_key=True)
#     ranking = Column(Integer, nullable=False)
#     title = Column(String, nullable=False)
#     author = Column(String, nullable=False)
#     image = Column(String, nullable=False)
#     isbn = Column(String, nullable=True)
#     price = Column(Integer, nullable=True)
#     caption = Column(String, nullable=True)
#     publisher = Column(String, nullable=True)
#     salesDate = Column(String, nullable=True)
#     score = Column(Integer, nullable=False)

# @asynccontextmanager
# async def session_scope():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()


# async def periodic_task():
#     async with session_scope() as session:
#         new_data = await merge_data()

#         stmt = select(Data2)
#         existing_data = await session.execute(stmt)
#         existing_data = existing_data.scalars().all()

#         if existing_data:
#             for existing, new in zip(existing_data, new_data):
#                 for key, value in new.items():
#                     if hasattr(existing, key):
#                         setattr(existing, key, value)
#         else:
#             filtered_new_data = [{key: value for key, value in item.items() if hasattr(Data2, key)} for item in new_data]
#             session.add_all([Data2(**item) for item in filtered_new_data])

#     return "Periodic task completed"


# SECRET_KEY = os.getenv("SECRET_KEY")
# MAX_TIME_DIFFERENCE = 300
# ALLOWED_IPS1 = os.getenv("ALLOWED_IPS1")
# ALLOWED_IPS2 = os.getenv("ALLOWED_IPS2")
# ALLOWED_IPS3 = os.getenv("ALLOWED_IPS3")
# ALLOWED_IPS4 = os.getenv("ALLOWED_IPS4")
# ALLOWED_IPS = [ALLOWED_IPS1, ALLOWED_IPS2, ALLOWED_IPS3, ALLOWED_IPS4]

# def generate_token(timestamp):
#     message = str(timestamp).encode()
#     signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
#     return base64.b64encode(signature).decode()

# def ip_in_network(ip, network):
#     return ip_address(ip) in ip_network(network)

# @app.before_request
# async def limit_remote_addr():
#     pass

# @app.route('/update', methods=['POST'])
# @rate_limit(5, timedelta(minutes=1))
# async def update():
#     token = request.headers.get('Authorization')
#     timestamp = request.headers.get('X-Timestamp')

#     if not token or not timestamp:
#         abort(401)

#     expected_token = generate_token(timestamp)

#     if not hmac.compare_digest(token, expected_token):
#         abort(401)

#     if abs(int(timestamp) - int(time.time())) > MAX_TIME_DIFFERENCE:
#         abort(401)

#     await periodic_task()

#     return "Update successful", 200

# @app.route("/hello")
# @rate_limit(5, timedelta(minutes=1))
# async def hello2():
#     # new_data = await periodic_task()
#     new_data = await merge_data()
#     return jsonify(new_data)

# # url確認用
# @app.route('/url')
# async def home():
#     url = request.base_url
#     return f'このページのURLは {url} です'


# # 定期的にアクセスする用
# @app.route('/access')
# @rate_limit(5, timedelta(minutes=1))
# async def access():
#     now_time = datetime.now()
#     return f'現在の時刻は {now_time}です！ '

# app.run(host='0.0.0.0', port=8080)








# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import asyncio
# from quart import Quart, request, abort, jsonify
# from sqlalchemy import Column, Integer, String, select
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import declarative_base, sessionmaker
# # from dotenv import load_dotenv
# import hmac
# import hashlib
# import base64
# import time
# import os
# from ipaddress import ip_address, ip_network
# from contextlib import asynccontextmanager

# from get_book_sales_ranking.data_fix.clean_up import merge_data

# # 本番用
# DATABASE_URL = os.environ.get("DATABASE_URL")
# # print("DATABASE_URL",DATABASE_URL)

# engine = create_async_engine(DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Base = declarative_base()

# class Data2(Base):
#     __tablename__ = 'data2'
#     id = Column(Integer, primary_key=True)
#     ranking = Column(Integer, nullable=False)
#     title = Column(String, nullable=False)
#     author = Column(String, nullable=False)
#     image = Column(String, nullable=False)
#     isbn = Column(String, nullable=True)
#     price = Column(Integer, nullable=True)
#     caption = Column(String, nullable=True)
#     publisher = Column(String, nullable=True)
#     salesDate = Column(String, nullable=True)
#     score = Column(Integer, nullable=False)

# @asynccontextmanager
# async def session_scope():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()


# async def periodic_task():
#     async with session_scope() as session:
#         new_data = await merge_data()

#         stmt = select(Data2)
#         existing_data = await session.execute(stmt)
#         existing_data = existing_data.scalars().all()

#         if existing_data:
#             for existing, new in zip(existing_data, new_data):
#                 for key, value in new.items():
#                     if hasattr(existing, key):
#                         setattr(existing, key, value)
#         else:
#             filtered_new_data = [{key: value for key, value in item.items() if hasattr(Data2, key)} for item in new_data]
#             session.add_all([Data2(**item) for item in filtered_new_data])

#     return "Periodic task completed"


# SECRET_KEY = os.getenv("SECRET_KEY")
# MAX_TIME_DIFFERENCE = 300
# ALLOWED_IPS1 = os.getenv("ALLOWED_IPS1")
# ALLOWED_IPS2 = os.getenv("ALLOWED_IPS2")
# ALLOWED_IPS3 = os.getenv("ALLOWED_IPS3")
# ALLOWED_IPS4 = os.getenv("ALLOWED_IPS4")
# ALLOWED_IPS = [ALLOWED_IPS1, ALLOWED_IPS2, ALLOWED_IPS3, ALLOWED_IPS4]

# def generate_token(timestamp):
#     message = str(timestamp).encode()
#     signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
#     return base64.b64encode(signature).decode()

# def ip_in_network(ip, network):
#     return ip_address(ip) in ip_network(network)


# # async def update(*, kw1, kw2, kw3):
# async def update():
#     token = request.headers.get('Authorization')
#     timestamp = request.headers.get('X-Timestamp')

#     if not token or not timestamp:
#         abort(401)

#     expected_token = generate_token(timestamp)

#     if not hmac.compare_digest(token, expected_token):
#         abort(401)

#     if abs(int(timestamp) - int(time.time())) > MAX_TIME_DIFFERENCE:
#         abort(401)

#     await periodic_task()

#     return "Update successful", 200

# if __name__ == "__main__":
#     asyncio.run(update())












# 本番用
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from quart import Quart, request, abort, jsonify
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv
import hmac
import hashlib
import base64
import time
import os
from ipaddress import ip_address, ip_network
from contextlib import asynccontextmanager

from get_book_sales_ranking.data_fix.clean_up import merge_data

class Config:
    def __init__(self, database_url=None, secret_key=None, allowed_ips=None, max_time_difference=300):
        self.database_url = database_url
        self.secret_key = secret_key
        self.allowed_ips = allowed_ips or []
        self.max_time_difference = max_time_difference

config = Config()

def initialize(database_url, secret_key, allowed_ips=None, max_time_difference=300):
    global config
    config = Config(database_url, secret_key, allowed_ips, max_time_difference)

    global engine
    engine = create_async_engine(config.database_url, echo=True)
    global AsyncSessionLocal
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Data2(Base):
    __tablename__ = 'data2'
    id = Column(Integer, primary_key=True)
    ranking = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    image = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    caption = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    salesDate = Column(String, nullable=True)
    score = Column(Integer, nullable=False)

    # 追加部分　2024/08/09　18:19
    page = Column(String, nullable=True)
    booktype = Column(String, nullable=True)

@asynccontextmanager
async def session_scope():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


async def periodic_task():
    async with session_scope() as session:
        new_data = await merge_data()

        stmt = select(Data2)
        existing_data = await session.execute(stmt)
        existing_data = existing_data.scalars().all()

        if existing_data:
            for existing, new in zip(existing_data, new_data):
                for key, value in new.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
        else:
            filtered_new_data = [{key: value for key, value in item.items() if hasattr(Data2, key)} for item in new_data]
            session.add_all([Data2(**item) for item in filtered_new_data])

    return "Periodic task completed"



def generate_token(timestamp):
    message = str(timestamp).encode()
    signature = hmac.new(config.secret_key.encode(), message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def ip_in_network(ip, network):
    return ip_address(ip) in ip_network(network)


async def update(*, token, timestamp):
# async def update():



    # token = request.headers.get('Authorization')
    # timestamp = request.headers.get('X-Timestamp')

    if not token or not timestamp:
        abort(401)

    expected_token = generate_token(timestamp)

    if not hmac.compare_digest(token, expected_token):
        abort(401)

    if abs(int(timestamp) - int(time.time())) > config.max_time_difference:
        abort(401)

    await periodic_task()

    return "Update successful", 200


# if __name__ == "__main__":
#     asyncio.run(update())



# from get_book_sales_ranking.api.rakuten_api import fetch_rakuten

# async def tameshi():
#     kari = await fetch_rakuten()
#     print("kari",kari)

# if __name__ == "__main__":
#     asyncio.run(tameshi())

