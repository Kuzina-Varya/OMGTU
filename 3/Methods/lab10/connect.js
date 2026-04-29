const { MongoClient } = require('mongodb');

async function run() {
  const uri = "mongodb://localhost:27017";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    console.log("Успешное подключение к серверу MongoDB!");
    
    const db = client.db("transport_company");
    console.log("Текущая база данных:", db.databaseName);
    
    // Список коллекций
    const collections = await db.listCollections().toArray();
    console.log("Коллекции:", collections.map(c => c.name));
    
  } catch (err) {
    console.error("Ошибка подключения:", err);
  } finally {
    await client.close();
    console.log("Соединение закрыто");
  }
}

run().catch(console.dir);