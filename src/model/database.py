import sqlite3 as sql
from sqlite3 import Error
from src.config import config


class Database:
    
    conn = None
    db_file = None
    
    ####################################################################################

    def __init__(self, db_file):
        self.db_file = db_file
        # Generic connection which is used by all the member functions of the class
        self.conn = self.connect_db()

    ####################################################################################


    def connect_db(self):
        """ 
        Create a database connection to a SQLite database 

        """
        try:
            conn = sql.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    ####################################################################################


    def create_table(self):
        '''
        Create Cookies table {id  , cookie_id ,signature ,ip , ip34 , timestamp} if not created throw error

        '''

        try:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS cookies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cookie_id TEXT DEFAULT NULL,
                signature TEXT DEFAULT NULL,
                ip TEXT DEFAULT NULL,
                ip34 TEXT DEFAULT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                
                );
                ''')
            # Fingerprint table to store all the attributes of the fingerprint
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cookie_enabled TEXT DEFAULT 'unknown',
                user_agent TEXT NOT NULL,
                http_accept TEXT NOT NULL,
                plugins TEXT ,
                fonts TEXT ,
                timezone TEXT  DEFAULT NULL,
                video TEXT DEFAULT NULL,
                supercookies TEXT DEFAULT NULL,
                canvas_hash TEXT DEFAULT NULL,
                dnt_enabled TEXT DEFAULT NULL,
                webgl_hash TEXT DEFAULT NULL,
                language TEXT DEFAULT NULL,
                touch_support TEXT DEFAULT NULL,
                activity TEXT DEFAULT NULL,
                timezone_string TEXT DEFAULT NULL,
                webgl_vendor_renderer TEXT DEFAULT NULL,
                ad_block TEXT DEFAULT NULL,
                audio TEXT DEFAULT NULL,
                cpu_class TEXT DEFAULT NULL,
                hardware_concurrency TEXT DEFAULT NULL,
                device_memory TEXT DEFAULT NULL,
                load_remote_fonts TEXT DEFAULT NULL,
                signature TEXT NOT NULL DEFAULT '',
                count INTEGER NOT NULL DEFAULT 1
                );
                
                ''')

            # Signature table for storing signature

            self.conn.execute('''
                              
                CREATE TABLE IF NOT EXISTS signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signature TEXT UNIQUE DEFAULT NULL,
                fingerprint_id INTEGER NOT NULL REFERENCES fingerprints(id)
                );
                ''')

            # Total table to strore counts of each attribute

            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS totals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variable TEXT UNIQUE NOT NULL DEFAULT '',
                value TEXT NOT NULL DEFAULT '',
                total INTEGER NOT NULL DEFAULT 0
                );
                
                '''
            )

            self.conn.commit()
            self.conn.close()
        except Error as e:
            print(e)

    ####################################################################################


    def count_sightings(self, cookie_id, signature):
        '''
        Function to get all the sightings from the cookies table whose cookie_id is cookie_id and signature is signature

        '''

        try:
            conn = self.connect_db()
            count = conn.execute('''
                                        SELECT COUNT(cookie_id) FROM cookies WHERE cookie_id = ? AND signature = ?
                                        ''', (cookie_id, signature)).fetchone()[0]
            conn.close()
            return count
        except Error as e:
            print(e)
        
    #####################################################################################
    
    def record_sighting(self, cookie, signature, ip, google_style_ip):
        '''
        Function to put (cookie , signature , ip , google_style_ip) in the cookies table

        '''
        conn = self.connect_db()
        conn.execute(''' 
                           INSERT INTO cookies (cookie_id , signature , ip , ip34) VALUES (?,?,?,?)
                           ''', (cookie, signature, ip, google_style_ip))
        conn.commit()
        conn.close()
        
    #####################################################################################

    def update_totals_table(self, attributes, signature):
        '''
        Function to update the totals table by incrementing the count of each attribute by 1

        '''
        conn = self.connect_db()
        try:
            query = """ INSERT INTO totals (variable , value , total) VALUES (?,?,1) ON CONFLICT(value) DO UPDATE SET total = total + 1 """
            conn.execute(query, ('count', ''))

            for attribute in attributes:
                conn.execute(query, (attribute, attributes[attribute]))

            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()


    #####################################################################################

    def _record_fingerprint_helper(self ,attributes):
        '''
        Functiont to insert attributes in fingerprints table
        
        '''
        
        try:
            conn = self.connect_db()
            query_str = '''INSERT INTO fingerprints (cookie_enabled , user_agent , http_accept , plugins , fonts , timezone , video , supercookies , canvas_hash , dnt_enabled , webgl_hash , language , touch_support , activity , timezone_string , webgl_vendor_renderer , ad_block , audio , cpu_class , hardware_concurrency , device_memory , load_remote_fonts , signature) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            ON CONFLICT (signature) DO UPDATE SET count = count + 1
                        '''
            conn.execute(query_str, (attributes.values()))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
    
    #####################################################################################
    
    def _record_signature(self , signature):
        '''
        Function to record signature in signatures table
    
        '''
        
        try:
            conn = self.connect_db()
            conn.execute('''INSERT INTO signatures (signature) VALUES (?)''', (signature,))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

    #####################################################################################
    
    
    def record_fingerprint(self , attribute , signature):
        '''
        Function to record attribute and signature in fingerprints and signatures table
        
        '''
        try:
            self._record_fingerprint_helper(attribute)
            self._record_signature(signature)
        except Error as e:
            print(e)
        
        