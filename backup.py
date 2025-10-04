import os
from dotenv import load_dotenv
import subprocess
from datetime import datetime

load_dotenv()

def backup_database():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    dbname = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"D:\\Database\\bookstore_backup_{timestamp}.dump"

    command = [
        r"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe",
        "-h", host,
        "-p", port,
        "-U", user,
        "-d", dbname,
        "-f", backup_file
    ]

    env = os.environ.copy()
    env["PGPASSWORD"] = password

    subprocess.run(command, check=True, env=env)
    return backup_file
