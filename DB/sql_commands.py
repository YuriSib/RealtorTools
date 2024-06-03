create_db = '''CREATE TABLE IF NOT EXISTS users 
                (tg_id INTEGER PRIMARY KEY, 
                name TEXT, 
                filter_1 TEXT, 
                filter_2 TEXT, 
                region TEXT, 
                url TEXT)'''