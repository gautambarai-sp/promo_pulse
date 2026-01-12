# 🧪 Revenue vs Margin Chart - Quick Test Guide

## ✅ Pre-Launch Checklist

### Code Verification
- [x] `create_revenue_margin_chart()` function implemented (lines 228-413)
- [x] Chart display section updated (lines 738-805)
- [x] Sidebar controls added (lines 740-741)
- [x] Summary statistics implemented (lines 766-783)
- [x] Data table expansion added (lines 785-794)
- [x] No syntax errors found
- [x] All imports present

---

## 🚀 How to Run

### Option 1: From Terminal
```bash
cd "c:\Users\Aishwarya Patil\Downloads\Group Assignment\Group Assignment"
streamlit run app.py
```

### Option 2: From VS Code
1. Open Terminal (Ctrl + `)
2. Run: `streamlit run app.py`
3. Browser opens automatically to `http://localhost:8501`

---

## 🎯 What to Test

### 1. Chart Display
- [ ] Chart appears on Trends tab
- [ ] Chart has title "Revenue vs Margin Trend"
- [ ] Blue revenue bars visible
- [ ] Pink margin line with dots visible
- [ ] Chart is responsive and fills screen width

### 2. Data Integrity
- [ ] Data is from May-September 2024 only
- [ ] Weekly aggregation (7 data points expected)
- [ ] Revenue values > 0 (not negative)
- [ ] Margin % between 0-100%

### 3. Hover Functionality
- [ ] Hover over bars shows tooltip
- [ ] Tooltip shows: Week of [date]
- [ ] Tooltip shows: Revenue: AED [amount]
- [ ] Tooltip shows: Margin: [%]
- [ ] Format is correct (commas for thousands)

### 4. Interactive Features
- [ ] **Zoom:** Click and drag to zoom on specific area
- [ ] **Pan:** After zoom, can drag to pan
- [ ] **Range Slider:** Bottom of chart has date selector
- [ ] **Range Slider:** Drag to change visible date range
- [ ] **Legend:** Click legend items to show/hide data
- [ ] **Download:** Camera icon in top-right works

### 5. Average Lines
- [ ] Sidebar has "Show Average Lines" checkbox
- [ ] When ON: Blue dashed line visible (avg revenue)
- [ ] When ON: Pink dashed line visible (avg margin)
- [ ] When OFF: Average lines disappear
- [ ] Lines are labeled with values

### 6. Peak Annotations
- [ ] Highest revenue week marked with 📈 label
- [ ] Highest margin week marked with 📈 label
- [ ] Annotations have arrows pointing to peaks
- [ ] Text is readable and positioned well

### 7. Summary Statistics
- [ ] 4 metric cards visible below chart
- [ ] "Average Revenue" card shows value in AED
- [ ] "Average Margin" card shows percentage
- [ ] "Weeks Tracked" shows number
- [ ] "Total Revenue" shows AED total

### 8. Data Table
- [ ] "📋 View Weekly Data" section visible
- [ ] Can expand/collapse the table
- [ ] Table shows three columns: Week, Revenue, Margin
- [ ] Data matches chart values
- [ ] Numbers are formatted correctly

### 9. Sidebar Controls
- [ ] "Smooth Margin Trend" checkbox visible
- [ ] Both checkboxes are interactive
- [ ] Changes apply without page refresh

### 10. Export Function
- [ ] Hover over chart shows toolbar
- [ ] Camera/download icon visible in toolbar
- [ ] Click download → file named "revenue_vs_margin_trend.png" downloads
- [ ] Image quality is good (1000x600px)

---

## 🔍 Data Points to Verify

### Expected Data Structure
```
May 1-7, 2024:     Revenue: 4,500-5,500 AED  |  Margin: 55-65%
May 8-14, 2024:    Revenue: 4,200-5,200 AED  |  Margin: 55-65%
May 15-21, 2024:   Revenue: 4,800-5,800 AED  |  Margin: 55-65%
May 22-28, 2024:   Revenue: 5,000-6,000 AED  |  Margin: 55-65%
May 29-31 + Jun:   Revenue: 4,400-5,400 AED  |  Margin: 55-65%
...
(Continue through September 30)
```

### Validation Points
- Margin % should never exceed 100%
- Revenue should be positive
- No zero or null values in chart
- Consistent data across all 22+ weeks

---

## 🐛 Troubleshooting

### Issue: Chart doesn't appear
**Solution:**
- Check if data exists for May-September 2024
- Verify sales data is loaded correctly
- Check console for error messages (Terminal tab)

### Issue: No data tooltip on hover
**Solution:**
- Ensure chart is fully loaded
- Try refreshing the page (F5)
- Check browser console for JavaScript errors

### Issue: Download button missing
**Solution:**
- Hover over chart (don't click on data)
- Ensure Plotly is up to date
- Try different browser

### Issue: Average lines not showing
**Solution:**
- Check "Show Average Lines" checkbox in sidebar
- Verify Streamlit app is running latest code
- Try refreshing page

### Issue: Range slider not working
**Solution:**
- Scroll down to see full range slider
- Try clicking and dragging on dates
- Ensure chart height is sufficient

---

## 📊 Key Metrics to Validate

### Calculate Expected Average Revenue
```
Sum of all weekly revenues / Number of weeks = Average Revenue
```

### Calculate Expected Average Margin
```
Sum of all margin percentages / Number of weeks = Average Margin %
```

### Compare to Display
- Displayed average revenue should match calculation
- Displayed average margin should match calculation
- Difference < 0.01% is acceptable (rounding)

---

## ✨ Expected Chart Appearance

```
┌─────────────────────────────────────┐
│  Revenue vs Margin Trend            │  ← Title
│  May-September 2024                 │
├─────────────────────────────────────┤
│                                     │
│  Revenue (AED)  ▓▓▓▓▓▓              │  ← Blue bars (left Y-axis)
│              ▓▓▓▓▓▓▓                │
│            ▓▓▓▓▓▓▓▓               │
│  ━━━━━━━━━━━ (avg revenue line)   │  ← Dashed blue line
│                                     │
│             ●―●―●―●―●              │  ← Pink line with dots (right Y-axis)
│         ━━━━━━━━━━━━━━━ (avg)     │  ← Dashed pink line
│                                     │
│  ┌─────────────────────────────┐   │
│  │ May 1  May 15  Jun 1  Jun 15│   │  ← X-axis dates
│  └─────────────────────────────┘   │
│     [═══════ Range Slider ═════]   │
│                                     │
└─────────────────────────────────────┘

Below chart:
┌──────────┬────────┬─────────┬───────┐
│ 📈 Avg   │ 💰 Avg │ 📊 Weeks│ 💵    │
│ Revenue  │ Margin │ Tracked │ Total │
│ 5,200 AED│ 60.2%  │   22    │ 114.4K│
└──────────┴────────┴─────────┴───────┘

Data Table:
📋 View Weekly Data ▼
┌────────────┬──────────┬────────┐
│ Week       │ Revenue  │ Margin │
├────────────┼──────────┼────────┤
│ May 01     │ 5,200    │ 60.0%  │
│ May 08     │ 4,800    │ 59.5%  │
│ May 15     │ 5,400    │ 60.5%  │
│ ...        │ ...      │ ...    │
└────────────┴──────────┴────────┘
```

---

## 🎯 Post-Test Actions

### If All Tests Pass ✅
1. Take screenshot of chart
2. Test export PNG file
3. Document any minor improvements needed
4. Chart is production-ready!

### If Issues Found 🔧
1. Note exact issue and steps to reproduce
2. Check error messages in Terminal
3. Review app.py syntax around issue
4. Verify data integrity
5. Apply fix and retest

---

## 📞 Support Tips

### Chart Not Showing?
- Run: `streamlit run app.py --logger.level=debug`
- Check terminal for detailed error messages

### Performance Issues?
- Chart should load in <1 second
- If slower, check sales data size
- Verify system RAM available

### Want to Customize?
- Edit colors in `create_revenue_margin_chart()` line 260-280
- Adjust date range in lines 242-248
- Change aggregation from 'W' to 'D' or 'M' (line 250)

---

## 🎓 Learning Points

1. **Dual Y-axes:** `make_subplots(specs=[[{"secondary_y": True}]])`
2. **Weekly Aggregation:** `.dt.to_period('W').apply(lambda r: r.start_time)`
3. **Annotations:** `fig.add_annotation()` for labels and arrows
4. **Formatting:** `.strftime()` for dates, comma formatting for currency
5. **Export:** Plotly's built-in PNG download via config dict

---

**Chart Implementation Complete! Ready for Testing.** 🚀
