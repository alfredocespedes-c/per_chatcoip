import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "incendios_dummy.db"
REGIONES={"Arica y Parinacota":["Arica","Putre"],"Tarapacá":["Iquique","Pozo Almonte"],"Antofagasta":["Antofagasta","Calama"],"Atacama":["Copiapó","Vallenar"],"Coquimbo":["La Serena","Ovalle"],"Valparaíso":["Valparaíso","Quilpué"],"Metropolitana":["Santiago","Melipilla"],"O'Higgins":["Rancagua","Pichilemu"],"Maule":["Talca","Constitución"],"Ñuble":["Chillán","Yungay"],"Biobío":["Concepción","Los Ángeles","Hualqui"],"La Araucanía":["Temuco","Angol"],"Los Ríos":["Valdivia","Panguipulli"],"Los Lagos":["Puerto Montt","Osorno"],"Aysén":["Coyhaique","Chile Chico"],"Magallanes":["Punta Arenas","Puerto Natales"]}

def random_date():
    start=datetime(2024,1,1); end=datetime.now(); return start+timedelta(seconds=random.randint(0,int((end-start).total_seconds())))
def random_area():
    r=random.random()
    if r<.70:return round(random.uniform(.1,50),2)
    if r<.90:return round(random.uniform(50,400),2)
    if r<.98:return round(random.uniform(400,1000),2)
    return round(random.uniform(1000,5000),2)

random.seed(42)
conn=sqlite3.connect(DB_FILE)
conn.execute("DROP TABLE IF EXISTS incendios")
conn.execute("CREATE TABLE incendios (id INTEGER PRIMARY KEY, ubicacion TEXT NOT NULL, region TEXT NOT NULL, hectareas REAL NOT NULL, estado TEXT NOT NULL, fecha DATE NOT NULL)")
for i in range(1,101):
    region=random.choice(list(REGIONES)); ubicacion=random.choice(REGIONES[region])
    conn.execute("INSERT INTO incendios VALUES (?,?,?,?,?,?)",(i,ubicacion,region,random_area(),random.choice(["Controlado","No controlado"]),random_date().strftime("%Y-%m-%d")))
conn.commit(); conn.close()
print(f"Base dummy creada: {DB_FILE} (100 incendios)")
