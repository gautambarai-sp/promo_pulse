# 🤖 AI Insights Quick Reference

## Quick Setup (2 minutes)

### 1️⃣ Get API Key
Visit: https://aistudio.google.com/app/apikey → Copy key

### 2️⃣ Add to Secrets
Edit `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "paste_your_key_here"
```

### 3️⃣ Install Package
```bash
pip install google-generativeai
```

### 4️⃣ Run Dashboard
```bash
streamlit run app.py
```

---

## 📍 Where to Find AI Features

| Location | Feature | Icon | Description |
|----------|---------|------|-------------|
| Executive Suite (Top) | KPI Insights | 🔮 | Strategic analysis of revenue, margin, returns |
| Trends Section | Trend Analysis | 🤖 | Pattern analysis and predictions |
| Inventory Section | Inventory Analysis | 🤖 | Stock level and reorder recommendations |
| Data Quality Section | Quality Analysis | 🤖 | Data quality rating and priorities |

---

## 🎯 What Each AI Feature Does

### 🔮 Executive Suite - Deep Insights
- ✓ Analyzes KPIs (revenue, margin, returns)
- ✓ Compares to industry benchmarks
- ✓ Identifies top 2 priorities
- ✓ Provides 2-3 actionable recommendations

### 📈 Trends - AI Analysis
- ✓ Finds patterns in revenue/margin
- ✓ Detects anomalies or outliers
- ✓ Predicts next period trends
- ✓ Quantifies observations

### 📦 Inventory - AI Analysis
- ✓ Assesses overall inventory health
- ✓ Identifies reorder priorities
- ✓ Recommends stockout prevention
- ✓ Analyzes stock distribution

### 🔍 Data Quality - AI Analysis
- ✓ Rates overall data quality (Good/Fair/Poor)
- ✓ Identifies critical issues
- ✓ Suggests quick fixes
- ✓ Prioritizes by impact

---

## ⚡ Performance

| Metric | Time |
|--------|------|
| First AI Call | 2-10 sec |
| Subsequent Calls | 1-5 sec |
| Dashboard Load | Not affected |
| API Initialization | <100ms |

---

## ✅ Verification Checklist

- [ ] API key obtained from Google AI Studio
- [ ] GEMINI_API_KEY added to secrets.toml
- [ ] google-generativeai installed (`pip install google-generativeai`)
- [ ] Dashboard runs without errors
- [ ] 🤖 icons visible throughout dashboard
- [ ] Expandable AI sections open when clicked
- [ ] AI responses appear after 2-10 seconds

---

## 🐛 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| "API key not found" | Check `.streamlit/secrets.toml` has GEMINI_API_KEY |
| "Could not initialize AI" | Verify `google-generativeai` is installed |
| AI sections don't appear | Restart Streamlit: `ctrl+C` then `streamlit run app.py` |
| Slow responses | Normal on first call; API may be busy |
| No internet | Check connection; AI requires internet |

---

## 📊 What Gets Analyzed

### Executive KPIs
- Net revenue & margin
- Return rates & budget
- Simulation results
- Constraint violations

### Trends Data
- Weekly revenue
- Margin percentages
- Revenue ranges
- Trend patterns

### Inventory Data
- Stock on hand (avg/min/max)
- Median stock levels
- Stock deviation
- Product count

### Data Quality
- Total issues
- Issue types
- Most common issues
- Issues per type average

---

## 🔐 Security Reminder

⚠️ **IMPORTANT:**
1. NEVER commit `.streamlit/secrets.toml` to git
2. Add it to `.gitignore` first
3. Generate new API key if accidentally exposed
4. Use different keys for dev/production

---

## 📞 Common Questions

**Q: Is this free?**
A: Yes! Gemini API has a free tier with generous limits.

**Q: How often can I use it?**
A: Unlimited within rate limits (60 req/min, 1.5M tokens/day).

**Q: Does it slow down the dashboard?**
A: No - AI runs in background; dashboard is responsive.

**Q: Can I use it offline?**
A: No - requires internet connection to Google API.

**Q: What if API goes down?**
A: Dashboard works normally; AI features just show "unavailable".

---

## 🚀 Next Steps

1. Add API key to secrets.toml
2. Run `python test_ai_integration.py` to verify
3. Launch dashboard with `streamlit run app.py`
4. Look for 🤖 and 🔮 icons
5. Click expandable sections to see AI insights

---

**Version:** 1.0 | **Updated:** Jan 12, 2026
