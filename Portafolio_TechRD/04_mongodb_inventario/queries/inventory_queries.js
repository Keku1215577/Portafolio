use("portfolio_inventory");

// 1. Productos con stock bajo
db.products.find(
  { $expr: { $lte: ["$stock", "$min_stock"] } },
  { _id: 0, sku: 1, name: 1, stock: 1, min_stock: 1, warehouse: 1 }
).sort({ stock: 1 });

// 2. Valor total del inventario por producto
db.products.aggregate([
  { $match: { active: true } },
  {
    $project: {
      _id: 0,
      sku: 1,
      name: 1,
      stock: 1,
      inventory_value: { $multiply: ["$stock", "$cost"] }
    }
  },
  { $sort: { inventory_value: -1 } }
]);

// 3. Valor del inventario por categoría
db.products.aggregate([
  { $match: { active: true } },
  {
    $group: {
      _id: "$category",
      units: { $sum: "$stock" },
      inventory_value: { $sum: { $multiply: ["$stock", "$cost"] } }
    }
  },
  { $sort: { inventory_value: -1 } }
]);

// 4. Proveedores con mayor cantidad de productos
db.products.aggregate([
  { $match: { active: true } },
  {
    $group: {
      _id: "$supplier",
      product_count: { $sum: 1 },
      units: { $sum: "$stock" }
    }
  },
  { $sort: { units: -1 } }
]);

// 5. Inventario por ciudad y zona
db.products.aggregate([
  { $match: { active: true } },
  {
    $group: {
      _id: {
        city: "$warehouse.city",
        zone: "$warehouse.zone"
      },
      products: { $sum: 1 },
      units: { $sum: "$stock" }
    }
  },
  { $sort: { "_id.city": 1, units: -1 } }
]);

// 6. Ranking de margen unitario
db.products.aggregate([
  { $match: { active: true } },
  {
    $project: {
      _id: 0,
      sku: 1,
      name: 1,
      margin_pct: {
        $multiply: [
          {
            $divide: [
              { $subtract: ["$price", "$cost"] },
              "$price"
            ]
          },
          100
        ]
      }
    }
  },
  { $sort: { margin_pct: -1 } }
]);

// 7. Índices recomendados para consultas frecuentes
db.products.createIndex({ sku: 1 }, { unique: true });
db.products.createIndex({ category: 1 });
db.products.createIndex({ "warehouse.city": 1 });
db.products.createIndex({ supplier: 1 });
