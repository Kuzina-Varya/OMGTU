const { MongoClient } = require('mongodb');

async function run() {
  const uri = "mongodb://localhost:27017";
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("transport_company");
    const shipments = db.collection("shipment");

    console.log("=== Агрегация: Сумма бонусов по водителям ===");

    const pipeline = [
      { $unwind: "$crewassignment" },
      {
        $group: {
          _id: "$crewassignment.driver_id",
          driver_name: { $first: "$crewassignment.full_name" },
          total_bonus: { $sum: "$crewassignment.bonus" }
        }
      },
      { $sort: { total_bonus: -1 } }
    ];

    const results = await shipments.aggregate(pipeline).toArray();
    results.forEach(r => {
      console.log(`Водитель: ${r.driver_name}, Сумма бонусов: ${r.total_bonus}`);
    });

  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

run().catch(console.dir);