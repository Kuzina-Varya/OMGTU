const { MongoClient } = require('mongodb');

async function run() {
  const uri = "mongodb://localhost:27017";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("transport_company");
    const drivers = db.collection("driver");

    // 1. CREATE (Вставка одного документа)
    console.log("=== Вставка нового водителя ===");
    
    // ИСПРАВЛЕНИЕ: Сначала получаем уровень опыта, потом берем _id
    const level = await db.collection("experience_level").findOne({description: "Новичок"});
    const newDriver = {
      driver_id: 5,
      full_name: "Смирнов Иван Иванович",
      experience_level_ref: level._id
    };
    
    const insertResult = await drivers.insertOne(newDriver);
    console.log("Вставлен документ с ID:", insertResult.insertedId);

    // 2. READ (Чтение всех документов)
    console.log("\n=== Все водители ===");
    const allDrivers = await drivers.find().toArray();
    allDrivers.forEach(d => console.log(d.full_name));

    // 3. UPDATE (Обновление документа)
    console.log("\n=== Обновление водителя ID 5 ===");
    const updateResult = await drivers.updateOne(
      { driver_id: 5 },
      { $set: { full_name: "Смирнов Иван Иванович (обновлен)" } }
    );
    console.log("Обновлено документов:", updateResult.modifiedCount);

    // 4. DELETE (Удаление документа)
    console.log("\n=== Удаление водителя ID 5 ===");
    const deleteResult = await drivers.deleteOne({ driver_id: 5 });
    console.log("Удалено документов:", deleteResult.deletedCount);

  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

run().catch(console.dir);