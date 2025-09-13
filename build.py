import requests
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建SQLAlchemy连接
# 替换为你的SQL Server连接字符串
# 格式类似于'mssql+pyodbc://username:password@server/database_name?driver=ODBC+Driver+17+for+SQL+Server'
DATABASE_URL = 'mysql+mysqlconnector://root:sql123@localhost:3306/steam_test'
engine = create_engine(DATABASE_URL, echo=True)  # 设为True以打印SQLAlchemy执行的SQL语句
Base = declarative_base()

# 定义数据库模型
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer)
    name = Column(String)
    description = Column(Text)
    # 添加其他你想要存储的游戏信息字段

# 创建表格（如果表格不存在）
Base.metadata.create_all(engine)

# 创建一个函数来获取并保存游戏信息
def save_game_info_to_db(game_id):
    # Steam API请求示例
    STEAM_API_KEY = '756A1F69D06DCC58F82E99E4C5B34E80'
    url = f'http://store.steampowered.com/api/appdetails?appids={game_id}&l=english'

    response = requests.get(url)
    if response.status_code == 200:
        game_data = response.json().get(str(game_id))

        if game_data.get('success'):
            data = game_data.get('data')

            # 提取游戏信息
            name = data.get('name')
            description = data.get('detailed_description')

            # 将游戏信息存入数据库
            session = sessionmaker(bind=engine)()
            new_game = Game(game_id=game_id, name=name, description=description)
            session.add(new_game)
            session.commit()
            session.close()
            print(f"Game '{name}' with ID '{game_id}' saved to the database.")
        else:
            print(f"Game with ID '{game_id}' not found.")
    else:
        print("Failed to fetch data from Steam API.")

# 调用函数并传入游戏ID以保存游戏信息到数据库
save_game_info_to_db(570)  # 传入游戏ID示例，可以更改为你想要的Steam游戏ID
