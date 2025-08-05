from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import sqlite3
from app.config.env import DB_PATH

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn, serde=JsonPlusSerializer(pickle_fallback=True))