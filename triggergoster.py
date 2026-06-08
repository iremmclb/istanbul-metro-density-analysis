import sqlite3

baglanti = sqlite3.connect('metrodensity.db')
trigger_kodu = baglanti.execute("SELECT sql FROM sqlite_master WHERE type='trigger'").fetchone()[0]
print(trigger_kodu)