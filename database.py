import sqlite3
import datetime

def standardize_distance(input_string):
    if "ft" in input_string:
        input_string = input_string.replace("ft", "").strip()
        meters = float(input_string) * 0.3048
    elif "yrd" in input_string or "yrds" in input_string:
        input_string = input_string.replace("yrds", "").replace("yrd", "").strip()
        meters = float(input_string) * 0.3048 * 3

    return meters

def percent_to_float(input_string):
    input_string = input_string.replace("%", "").strip()
    
    return (float(input_string)/100.0)


def cleanse_inputs(inputs):
    outputs = []

    for inp in inputs:
        if isinstance(inp,str):
            inp = inp.strip()
            if 'ft' in inp or 'yrd' in inp:
                inp = standardize_distance(inp)
            elif "%" in inp:
                inp = percent_to_float(inp)

        outputs.append(inp)

    return outputs

class Database:
    def __init__(self):
        self.con = sqlite3.connect('rnd.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = self.con.cursor()
        self.create_score_table()
        self.create_prox_table()

    '''CREATE the Scores TABLE'''
    def create_score_table(self):
        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS scores(id integer PRIMARY KEY AUTOINCREMENT, 
                                created_at timestamp NOT NULL, 
                                drill varchar(50) NOT NULL, 
                                session_id varchar(50) NOT NULL, 
                                score INTEGER NOT NULL,
                                distance INTEGER,
                                club varchar(50),
                                lie varchar(50),
                                other BLOB
                                )'''
                            )
    
    
    def create_prox_table(self):
        #'club', 'surface', 'distance', 'carry', 'stance', 'break'
        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS proximity(id integer PRIMARY KEY AUTOINCREMENT, 
                                created_at timestamp NOT NULL, 
                                drill varchar(50) NOT NULL, 
                                session_id varchar(50) NOT NULL,
                                prox INTEGER NOT NULL, 
                                distance INTEGER,
                                carry FLOAT,
                                club varchar(16),
                                surface varchar(16),
                                stance varchar(16),
                                break varchar(16),
                                other BLOB
                                )'''
                            )
    
    '''Add A Score'''
    def submit_score(self, drill, session_id, score, distance, club, lie, other=None):
        created_at = datetime.datetime.now()
        self.cursor.execute("INSERT INTO scores(created_at, drill, session_id, score, distance, club, lie, other) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (created_at, drill, session_id, score, distance, club, lie, other))
        self.con.commit()

        last_id = self.cursor.lastrowid

        # Getting the last entered item to add in the list
        created_score= self.cursor.execute("SELECT id, created_at, drill, session_id, score, distance, club, lie, other FROM scores WHERE id = ?", (last_id,)).fetchall()

        
        return created_score[-1]
    
    '''READ / GET the scores'''
    
    def get_session_scores(self, drill, session_id, limit = 10):
        # Getting CURRENT session_id scores
        scores = self.cursor.execute("SELECT id, created_at, drill, session_id, score, distance, club, lie, other FROM scores WHERE drill = ? and session_id = ? ORDER BY created_at ASC LIMIT ?", (drill, session_id, limit)).fetchall()

        return scores

    def get_historical_scores(self, drill, session_id, limit = 5):
        # Getting scores that are NOT the current session_ID
        scores = self.cursor.execute(
            '''
            SELECT session_id, MAX(created_at) as "[timestamp]", COUNT(id), AVG(score), GROUP_CONCAT(club), GROUP_CONCAT(lie) 
            FROM scores 
            WHERE drill = ? and session_id != ? 
            GROUP BY session_id
            ORDER BY MAX(created_at) DESC 
            LIMIT ?
            ''', (drill, session_id, limit)).fetchall()
        return scores
    
    def submit_prox(self, drill, session_id, prox, distance, carry, club, surface, stance, _break, other=None ):
        created_at = datetime.datetime.now()
        inputs = cleanse_inputs([created_at, drill, session_id, prox, distance, carry, club, surface, stance, _break, other])

        self.cursor.execute("INSERT INTO proximity(created_at, drill, session_id, prox, distance, carry, club, surface, stance, break, other) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            inputs)
        self.con.commit()

        last_id = self.cursor.lastrowid
        # Getting the last entered item to add in the list
        created_prox= self.cursor.execute("SELECT * FROM proximity WHERE id = ?", (last_id,)).fetchall()

        print(created_prox)



    '''Closing the connection '''
    def close_db_connection(self):
        self.con.close()