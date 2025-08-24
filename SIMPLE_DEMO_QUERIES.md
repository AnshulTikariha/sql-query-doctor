# 🚀 SQL QUERY DOCTOR - Simple Demo Queries

## 📝 **5 Essential Queries to Test Your SQL Query Doctor**

Copy and paste these queries into your SQL Query Doctor to see how it works!

---

## **Query 1: SELECT * Optimization**
**Input:**
```sql
SELECT * FROM users WHERE id = 1
```

**What it does:** Automatically suggests specific columns instead of SELECT * for better performance

---

## **Query 2: Safety Warning**
**Input:**
```sql
DELETE FROM users
```

**What it does:** Warns you about dangerous operations that could affect all rows

---

## **Query 3: IN to BETWEEN Conversion**
**Input:**
```sql
SELECT * FROM users WHERE id IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
```

**What it does:** Converts large IN clauses to BETWEEN for better performance

---

## **Query 4: Automatic LIMIT Addition**
**Input:**
```sql
SELECT id, name FROM users ORDER BY name
```

**What it does:** Automatically adds LIMIT clause to prevent large result sets

---

## **Query 5: Complex Query with Multiple Issues**
**Input:**
```sql
SELECT * FROM users u JOIN orders o ON u.id = o.user_id JOIN products p ON o.product_id = p.id WHERE u.active = 1 ORDER BY o.created_at
```

**What it does:** Shows how it handles multiple optimization rules at once

---

## **Query 6: Real-World E-commerce Query**
**Input:**
```sql
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE u.created_at >= '2024-01-01' GROUP BY u.id, u.name HAVING COUNT(o.id) > 0 ORDER BY total_spent DESC
```

**What it does:** Demonstrates handling of complex business queries with aggregations

---

## 🎯 **How to Use**

1. **Start your SQL Query Doctor** (run `./start.sh`)
2. **Open** http://localhost:4200
3. **Copy any query above** and paste it into the input field
4. **Click "Analyze Query"** to see the results
5. **Try different queries** to explore all features

## 🚀 **What You'll See**

- **Warnings** about potential performance issues
- **Optimized versions** of your queries
- **Specific suggestions** for improvement
- **Safety alerts** for dangerous operations

## 💡 **Perfect for:**

- **Code Reviews** - Check SQL before deployment
- **Learning** - Understand SQL best practices
- **Performance Tuning** - Optimize existing queries
- **Team Training** - Teach developers better SQL habits

---

**🎬 Ready for your YouTube demo! These 6 queries showcase all the key features of your SQL Query Doctor.**
