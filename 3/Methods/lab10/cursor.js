const { MongoClient } = require('mongodb');

async function run() {
  const uri = "mongodb://localhost:27017";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("transport_company");
    const shipments = db.collection("shipment");

    console.log("=== Итерация по курсору (shipment) ===");
    
    // Получаем курсор с сортировкой и лимитом
    const cursor = shipments.find().sort({ departure_date: 1 }).limit(2);

    // Вариант 1: forEach
    await cursor.forEach(doc => {
      console.log("Перевозка ID:", doc.shipment_id, "Груз:", doc.cargo_type);
    });

    // Вариант 2: while hasNext
    /*
    const cursor2 = shipments.find().limit(2);
    while (await cursor2.hasNext()) {
      const doc = await cursor2.next();
      console.log("Груз:", doc.cargo_type);
    }
    */

  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

run().catch(console.dir);