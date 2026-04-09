# 📋 PRESENTATION CHECKLIST CARD
*Print this and bring to presentation*

---

## ⏰ TIMELINE (15 minutes)
- [ ] 0:00-0:30 - Introduction
- [ ] 0:30-2:30 - Dataset overview  
- [ ] 2:30-5:30 - Training results
- [ ] 5:30-9:30 - Live prediction demo
- [ ] 9:30-11:30 - Visualization
- [ ] 11:30-14:30 - Q&A
- [ ] 14:30-15:00 - Wrap-up

---

## 🚀 QUICK COMMANDS
```bash
# Main demo
python3 demo_thuyet_trinh.py

# Visualization  
python3 demo_visualization.py

# Emergency
python3 demo_scripts/emergency_demo.py
```

---

## 🎯 KEY NUMBERS TO REMEMBER
- Dataset: **125,973** samples
- Features: **41**
- Best accuracy: **99.85%** (Gradient Boosting)
- Training time: **1.84** seconds
- Prediction speed: **15ms** per connection
- Attack types: **4** (DoS, R2L, U2R, Probe)

---

## 🔧 TROUBLESHOOTING
| Problem | Solution |
|---------|----------|
| Import error | Use `emergency_demo.py` |
| File not found | Run `setup_demo.sh` |
| Frozen screen | Ctrl+C, then `clear` |
| No response | Open new terminal |

---

## 💬 Q&A RESPONSES
**Q: Why this dataset?**
> "NSL-KDD is improved version of KDD'99, fixes redundancy issues"

**Q: Why not Deep Learning?**
> "99.85% already excellent, DL adds complexity for minimal gain"

**Q: Real-world deployment?**
> "Docker + Kubernetes, handles 1000+ conn/sec"

**Q: Handling new attacks?**
> "Anomaly detection generalizes to unknown patterns"

---

## ✨ CONFIDENCE BOOSTERS
- You prepared well ✓
- Code works (or backup ready) ✓
- You understand the topic ✓
- Audience wants you to succeed ✓

**Remember: Stay calm, speak clearly, enjoy!** 🎉