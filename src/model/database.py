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
                load_remote_fonts TEXT DEFAULT NULL,
                platform TEXT DEFAULT NULL,
                signature TEXT NOT NULL DEFAULT '',
                count INTEGER NOT NULL DEFAULT 1,
                UNIQUE (signature)
                );
                
                ''')

            # Signature table for storing desktop browser signatures and their count

            self.conn.execute('''
                              
                CREATE TABLE IF NOT EXISTS signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signature TEXT DEFAULT '',
                count INTEGER NOT NULL DEFAULT 0,
                UNIQUE (signature)
                );
                ''')

            # Signature table for storing mobile browser signatures and their count

            self.conn.execute('''
                                CREATE TABLE IF NOT EXISTS signatures_mobile (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                signature TEXT DEFAULT '',
                                count INTEGER NOT NULL DEFAULT 0,
                                UNIQUE (signature)
                                );
                                ''')

            # Total table to strore counts of each attribute

            self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS totals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variable TEXT NOT NULL DEFAULT '',
                value TEXT NOT NULL DEFAULT '',
                total INTEGER NOT NULL DEFAULT 0,
                UNIQUE (value)
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

        try:
            conn = self.connect_db()
            conn.execute(''' 
                           INSERT INTO cookies (cookie_id , signature , ip , ip34) VALUES (?,?,?,?)
                           ''', (cookie, signature, ip, google_style_ip))
            conn.commit()
        except Error as e:
            print('Error in Cookies table :', e)
        finally:
            conn.close()

    #####################################################################################

    def update_totals_table(self, attributes, signature):
        '''
        Function to update the totals table by incrementing the count of each attribute by 1

        '''

        conn = self.connect_db()
        try:
            query = """ INSERT INTO totals (variable , value , total) VALUES (?,?,1) ON CONFLICT(value) DO UPDATE SET total = total + 1 """
            conn.execute(query, ('count', 'count'))

            for attribute in attributes:
                conn.execute(query, (attribute, attributes[attribute]))

            conn.commit()
        except Error as e:
            print('Error in Totals table : ', e)
        finally:
            conn.close()

    #####################################################################################

    def _record_fingerprint_helper(self, attributes):
        '''
        Functiont to insert attributes in fingerprints table

        '''

        try:
            conn = self.connect_db()
            query_str = '''INSERT INTO fingerprints (cookie_enabled , user_agent , http_accept , plugins , fonts , timezone , video , supercookies , canvas_hash , webgl_hash , language , touch_support , activity , timezone_string , webgl_vendor_renderer , ad_block , audio , cpu_class , hardware_concurrency , load_remote_fonts ,platform, signature) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                            ON CONFLICT (signature) DO UPDATE SET count = count + 1
                        '''
            conn.execute(query_str, (str(attributes['cookie_enabled']),
                                     str(attributes['user_agent']),
                                     str(attributes['http_accept']),
                                     str(attributes['plugins']),
                                     str(attributes['fonts']),
                                     str(attributes['timezone']),
                                     str(attributes['video']),
                                     str(attributes['supercookies']),
                                     str(attributes['canvas_hash']),
                                     str(attributes['webgl_hash']),
                                     str(attributes['language']),   
                                    str(attributes['touch_support']),
                                    str(attributes['activity']), 
                                    str(attributes['timezone_string']), 
                                    str(attributes['webgl_vendor_renderer']), 
                                    str(attributes['ad_block']),
                                    str(attributes['audio']), 
                                    str(attributes['cpu_class']), 
                                    str(attributes['hardware_concurrency']), 
                                    str(attributes['loads_remote_fonts']),
                                    str(attributes['platform']),
                                    str(attributes['signature']),
                                    ))
            conn.commit()
        except Error as e:
            print('Error in Fingerprints table : ', e)
        finally:
            conn.close()

    #####################################################################################

    def _record_signature_desktop(self, signature):
        '''
        Function to record signature in signatures table

        '''

        try:
            conn = self.connect_db()
            conn.execute(
                '''INSERT INTO signatures (signature ,count) VALUES (? ,?) ON CONFLICT(signature) DO UPDATE SET count=count+1 ''', (signature,1))
            conn.commit()
        except Error as e:
            print('Error in Desktop Browser Signatures table : ', e)
        finally:
            conn.close()

    #####################################################################################

    def _record_signature_mobile(self, signature):
        '''
        Function to record signature in signatures table

        '''

        try:
            conn = self.connect_db()
            conn.execute(
                '''INSERT INTO signatures_mobile (signature ,count) VALUES (? ,1) ON CONFLICT(signature) DO UPDATE SET count=count+1 ''', (signature,))
            conn.commit()
        except Error as e:
            print('Error in Mobile Browser Signatures table : ', e)
        finally:
            conn.close()

    #####################################################################################

    def record_fingerprint(self, attributes, signature_desk, signature_mob):
        '''
        Function to record attribute and signature in fingerprints and signatures table

        '''

        try:
            self._record_fingerprint_helper(attributes)
            self._record_signature_desktop(signature_desk)
            self._record_signature_mobile(signature_mob)
        except Error as e:
            print('Error in Record_fingerprint Function :', e)

    #####################################################################################


    def fetch_count(self, signature , signature_mobile):
        '''
        Function to get count of particular signature from the respective table

        '''
        desk_count , desk_tot_count  = 0 , 0
        mob_count ,mob_tot_count = 0,0
        try:
            conn = self.connect_db()
            desk_count =  conn.execute(''' SELECT count FROM signatures WHERE signature =? ''', (signature,)).fetchone()[0]
            mob_count =  conn.execute(''' SELECT count FROM signatures_mobile WHERE signature =? ''', (signature_mobile,)).fetchone()[0]
            desk_tot_count = conn.execute(''' SELECT SUM(count) FROM signatures''').fetchone()[0]
            mob_tot_count = conn.execute(''' SELECT SUM(count) FROM signatures_mobile''').fetchone()[0]
            
            conn.close()

        except Error as e:
            print(e)

        return ([(desk_count,desk_tot_count),(mob_count,mob_tot_count)])

    #####################################################################################

    def fetch_individual_count(self, variable, value ):
        '''
        Helper function to get count of each variable from the table

        '''
        count = 0

        try:
            conn = self.connect_db()
            count = conn.execute('''
                                        SELECT total FROM totals WHERE variable =? AND value =?
                                        ''', (str(variable), str(value))).fetchone()[0]
            conn.close()
        except Error as e:
            print("error thrown from fetch_individual_count")
            print(e)

        return count

    #####################################################################################

    def fetch_count_totals_table(self):
        '''
        Function to get total count from totals table

        '''
        count = 0
        try:
            conn = self.connect_db()
            count = conn.execute('''
                                        SELECT total FROM totals WHERE value ='count'
                                        ''').fetchone()[0]
            conn.close()

        except Error as e:
            print(e)

        return count

    #####################################################################################
