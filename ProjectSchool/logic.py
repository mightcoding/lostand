import sqlite3
import numpy as np
import cv2

DATABASE = 'store.db'

class StoreManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS items (
                                item_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                date TEXT,
                                img TEXT
                            )''')

            conn.commit()

    def add_items(self, name, img, date):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("INSERT INTO items (name, date, img) VALUES (?, ?, ?)", (name,date,img))
            conn.commit()

    def date_selector(self,date,todaydate):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute("select * from store where date = ? - todaydate = ? > '3'", (date,todaydate)) #Где дата меньше 3 дней от нынешней
            conn.commit()

    def get_items(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * from items")
            return cur.fetchall()
        
    def get_items_data(self,item_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * from items where item_id = ?", (item_id))
            return cur.fetchall()
        
    def collage_creation(self,paths,output):
        img1 = cv2.imread(paths[0])
        img2 = cv2.imread(paths[1])
        img3 = cv2.imread(paths[2])
        img4 = cv2.imread(paths[3])

        img1 = cv2.resize(img1,(200,200))
        img2 = cv2.resize(img2,(200,200))
        img3 = cv2.resize(img3,(200,200))
        img4 = cv2.resize(img4,(200,200))

        col_1 = np.vstack([img1, img2])
        col_2 = np.vstack([img3, img4])


        collage = np.hstack([col_1, col_2])
        cv2.imwrite(output,collage)

    def diff_collage_creation(image_paths):
        images = []
        for path in image_paths:
            image = cv2.imread(path)
            images.append(image)

        num_images = len(images)
        num_cols = floor(sqrt(num_images)) # Поиск количество картинок по горизонтали
        num_rows = ceil(num_images/num_cols)  # Поиск количество картинок по вертикали
        # Создание пустого коллажа
        collage = np.zeros((num_rows * images[0].shape[0], num_cols * images[0].shape[1], 3), dtype=np.uint8)
        # Размещение изображений на коллаже
        for i, image in enumerate(images):
            row = i // num_cols
            col = i % num_cols
            collage[row*image.shape[0]:(row+1)*image.shape[0], col*image.shape[1]:(col+1)*image.shape[1], :] = image
        return collage


    


    def show_items(self):
        pass
    
if __name__ == '__main__':
    manager = StoreManager(DATABASE)
    # manager.create_tables()
    # data = [
    #     ("Кроссовки",  'розовый', "1.png")
    # ]
    # manager.add_items(data)
    manager.collage_creation()
    