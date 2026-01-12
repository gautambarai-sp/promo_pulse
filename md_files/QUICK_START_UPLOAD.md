# 🚀 Quick Start Guide - Custom Data Upload

## 30-Second Quickstart

### Option A: Use Sample Data (Recommended for First Run)
```bash
1. streamlit run app.py
2. Dashboard opens with pre-built data (default)
3. Click "🚀 Launch Simulation" in sidebar
4. Done! All features available
```

### Option B: Use Your Own Data
```bash
1. Prepare 4 CSV files (see format below)
2. streamlit run app.py
3. Select "📤 Upload Custom Data" in sidebar
4. Upload your 4 files
5. Click "🚀 Launch Simulation"
6. Done! Dashboard loads with your data
```

### Option C: Test with Sample Generated Data
```bash
1. python create_sample_dataset.py    # Creates sample_*.csv files
2. streamlit run app.py
3. Select "📤 Upload Custom Data"
4. Upload sample_products.csv, sample_stores.csv, 
   sample_sales.csv, sample_inventory.csv
5. Dashboard loads with generated sample data
```

---

## 📋 CSV File Checklist

Before uploading, have these 4 files ready:

### ✅ Required Files

#### 1. **Products CSV**
```csv
product_id,category,brand,unit_cost_aed
P001,Electronics,Samsung,150.50
P002,Fashion,Nike,45.75
```
**Columns:** product_id | category | brand | unit_cost_aed

#### 2. **Stores CSV**
```csv
store_id,city,channel
S001,Dubai,App
S002,Abu Dhabi,Web
```
**Columns:** store_id | city | channel

#### 3. **Sales CSV**
```csv
order_id,product_id,store_id,qty,selling_price_aed
ORD001,P001,S001,2,199.99
ORD002,P002,S002,1,89.99
```
**Columns:** order_id | product_id | store_id | qty | selling_price_aed

#### 4. **Inventory CSV**
```csv
product_id,store_id,stock_on_hand
P001,S001,150
P002,S002,75
```
**Columns:** product_id | store_id | stock_on_hand

### 📌 Optional File
- **Issues CSV** - For data quality tracking (can skip this)

---

## ⚠️ Important Rules

### IDs Must Match
- All `product_id` in Sales must exist in Products
- All `store_id` in Sales must exist in Stores
- All `product_id` in Inventory must exist in Products
- All `store_id` in Inventory must exist in Stores

### Column Names Matter
- Use **exact** spelling (case-sensitive)
- Don't use spaces in column names
- Required columns cannot be omitted

### Data Types Matter
- `qty`, `stock_on_hand` = Numbers only (integers)
- `selling_price_aed`, `unit_cost_aed` = Decimal numbers
- `product_id`, `store_id`, `order_id` = Text/String
- Channel = "App", "Web", or "Marketplace"
- City = "Dubai", "Abu Dhabi", or "Sharjah"

---

## 🔧 Common Preparation Steps

### In Excel / Google Sheets
1. Create your data or open existing data
2. Clean column names (remove spaces, special characters)
3. Delete empty rows
4. Ensure each column has the right data type
5. Save As → CSV format
6. Download CSV file

### Column Name Cleanup
| ❌ Wrong | ✅ Correct |
|---------|-----------|
| Product ID | product_id |
| Store_ID | store_id |
| Selling Price | selling_price_aed |
| Unit Cost | unit_cost_aed |
| Qty Ordered | qty |
| Stock Available | stock_on_hand |

---

## 🎬 Step-by-Step: Upload Custom Data

### Step 1: Start Dashboard
```bash
streamlit run app.py
```
Browser opens to http://localhost:8501

### Step 2: Select Upload Option
- Look at left sidebar
- Find "📊 Data Source" section
- Click radio button for "📤 Upload Custom Data"

### Step 3: Upload Files
You'll see upload boxes:
```
📦 Products CSV     |  🏪 Stores CSV
🛍️ Sales CSV       |  📊 Inventory CSV
```
- Click each box OR drag-drop files
- Order doesn't matter

### Step 4: Verify Upload
- Green checkmark ✅ appears when ready
- "Custom data loaded successfully!" message
- Dataset Information shows file counts

### Step 5: Use Dashboard
- All features now work with your data
- Click "🚀 Launch Simulation" to run scenarios
- Use filters and presets as normal

---

## 💡 Tips & Tricks

### For Large Datasets
- If dataset > 100k rows, performance may slow
- Solution: Use data for 1 month instead of 1 year
- Or sample 10-20% of your data

### For Testing
- Start with 10-50 records to verify format
- Then upload full dataset once format is correct

### For Troubleshooting
- If error occurs, check column names first
- Check that all IDs match across files
- Try pre-built data to confirm dashboard works

### For Multiple Datasets
- Can switch between datasets anytime
- Just select different radio button
- Re-upload new files when switching

---

## ✅ Validation Checklist

Before clicking upload, verify:

- [ ] All 4 CSV files ready
- [ ] Column names exactly match specification
- [ ] No empty columns in files
- [ ] No empty rows in middle of data
- [ ] product_id values are unique
- [ ] store_id values are unique
- [ ] order_id values are unique
- [ ] All product_ids in Sales exist in Products
- [ ] All store_ids in Sales exist in Stores
- [ ] Numeric columns don't contain text
- [ ] City names are: Dubai, Abu Dhabi, or Sharjah
- [ ] Channel names are: App, Web, or Marketplace

---

## 🆘 When Things Go Wrong

### Error: "Products missing columns: {'unit_cost_aed'}"
→ Check your Products CSV has column: `unit_cost_aed`

### Error: "Stores missing columns: {'city', 'channel'}"
→ Check your Stores CSV has columns: `city` and `channel`

### Error: "Please upload all required files"
→ Make sure you uploaded: Products, Stores, Sales, Inventory (Issues is optional)

### Dashboard shows "No data"
→ Check: Are product_ids in Sales also in Products?
→ Try: Select "Custom" preset to see all data

### Simulation button does nothing
→ Try: Pre-built data first to confirm dashboard works
→ Check: Your data has at least 10 orders

---

## 📚 Next Steps

After uploading, explore:

1. **Executive Suite** (💼 tab)
   - Revenue vs Margin trends
   - Product Performance Matrix
   - Geographic analysis

2. **Operations Command Center** (⚙️ tab)
   - Inventory analysis
   - Risk heat map
   - Data quality reports

3. **Simulations** (🎯 tab)
   - Test different discount scenarios
   - Optimize promotional budgets
   - Analyze stockout risks

---

## 📖 Full Documentation

For detailed information, see:
- `DATA_UPLOAD_GUIDE.md` - Complete upload guide
- `CUSTOM_UPLOAD_IMPLEMENTATION.md` - Technical details
- `README.md` - General dashboard documentation

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Prepare CSV format | 5 minutes |
| Upload files | 1 minute |
| Dashboard loads | 5-30 seconds |
| Create sample data | 2 minutes |
| First simulation | 3-5 minutes |

---

## 🎯 Success Indicators

You'll know it's working when you see:
- ✅ "Custom data loaded successfully!" message
- ✅ Dataset Information shows your row counts
- ✅ Dashboard displays without errors
- ✅ KPI cards show your data metrics
- ✅ Filters work with your categories/cities
- ✅ Simulation completes without errors

---

## 🤔 FAQ

**Q: Can I use Excel files directly?**
A: No, convert to CSV first. Excel → Save As → CSV format

**Q: What if I have missing data?**
A: Fill with 0 for numbers, "Unknown" for text

**Q: Can I upload data while dashboard is running?**
A: No, select upload option before starting. Or restart dashboard and reselect.

**Q: Will my data be stored on a server?**
A: No, data stays on your computer. Streamlit keeps it in memory only.

**Q: Can I upload non-CSV files?**
A: Only CSV files are supported. Convert Excel/JSON to CSV first.

**Q: How large can my dataset be?**
A: Tested up to 1M rows. Larger datasets may be slow.

---

## 🎓 Learning Path

1. **Day 1**: Try pre-built data
2. **Day 2**: Generate sample data and upload
3. **Day 3**: Prepare your own data
4. **Day 4**: Upload and explore results
5. **Day 5**: Run simulations and optimize

---

**Ready to start? Go to:**
```bash
streamlit run app.py
```

Happy analyzing! 📊✨
