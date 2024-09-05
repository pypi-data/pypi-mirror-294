import sqlite3

global direct
def setdirecritry(directory: str):
   global direct
   direct = directory

class table():
   def CreateTable(name: str, collumn: str):
     connect = sqlite3.connect(direct)
     cursor = connect.cursor()
     cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {name}(
        {collumn}
        );
        """
     )
     connect.commit()

   def AddToTable(table: str, items: list):
     connect = sqlite3.connect(direct)
     cursor = connect.cursor()
     values = '?'
     try:
      if len(items)!=1:values="?,"*int(len(items)-1)+"?"
     except:pass
     cursor.execute(f"INSERT INTO {table} VALUES({values})", items)
     connect.commit()

   def DeleteFromTable(table: str, collumn: str, target: list):
      connect = sqlite3.connect(direct)
      cursor = connect.cursor()
      cursor.execute(f"SELECT {collumn} FROM {table}")
      x = cursor.fetchall()
      for i in x:
         if i[0] == target[0]:
            cursor.execute(f"DELETE FROM {table} WHERE {collumn} = ?", target)
            connect.commit()

   def Edit(table_name: str, collumn: str, target: list, item):
      connect = sqlite3.connect(direct)
      cursor = connect.cursor()
      cursor.execute(f"SELECT * FROM {table_name}")
      x = cursor.fetchall()
      buff,items,count = [],[],0
      for i in x:
         for j in range(0,len(i)):
            if i[j] == target:
               buff+=i
               count=j
               cursor.execute(f"DELETE FROM {table_name} WHERE {collumn} = ?", [target])
               connect.commit()
               break
      for k in range(len(buff)):
         if k != count:
            items.append(buff[k])
         else:
            items.append(item)
      table.AddToTable(table_name, items)
      connect.commit()

class search():
   def item(table: str, target: list) -> list:
      connect = sqlite3.connect(direct)
      cursor = connect.cursor()
      cursor.execute(f"SELECT * FROM {table}")
      result = []
      x = cursor.fetchall()
      for i in x:
         y = len(i)
         for j in range(y):
            if i[j] == target:
               result.append(i)
      return result