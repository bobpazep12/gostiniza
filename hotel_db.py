import sqlite3
from datetime import datetime

class HotelDB:
    def __init__(self, db_name="hotel.db"):
        self.db_name = db_name
        self.create_tables()
    
    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                price_per_night REAL NOT NULL,
                amenities TEXT,
                image TEXT,
                status TEXT DEFAULT 'свободен',
                rating REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                passport_series TEXT,
                passport_number TEXT,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                guests_count INTEGER NOT NULL,
                services TEXT,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'активно',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT NOT NULL,
                FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                guest_name TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        self._add_sample_data()
        conn.close()
    
    def _add_sample_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM rooms")
        if cursor.fetchone()[0] == 0:
            test_rooms = [
                ("101", "Стандарт", 2, 2500, "Wi-Fi, TV, душ", "", "свободен"),
                ("102", "Стандарт", 2, 2500, "Wi-Fi, TV, душ", "", "свободен"),
                ("103", "Стандарт+", 2, 3000, "Wi-Fi, TV, душ, кондиционер", "", "свободен"),
                ("201", "Полулюкс", 3, 3500, "Wi-Fi, TV, душ, кондиционер, холодильник", "", "свободен"),
                ("202", "Полулюкс", 3, 3500, "Wi-Fi, TV, душ, кондиционер, холодильник", "", "свободен"),
                ("301", "Люкс", 4, 5000, "Wi-Fi, TV, джакузи, кондиционер, мини-бар", "", "свободен"),
                ("302", "Люкс", 4, 5000, "Wi-Fi, TV, джакузи, кондиционер, мини-бар", "", "свободен"),
                ("401", "Президентский люкс", 6, 10000, "Wi-Fi, TV, джакузи, сауна, мини
