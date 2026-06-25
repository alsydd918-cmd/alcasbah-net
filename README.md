# 🏰 نظام القلعة نت - AlCasbah Net

## نظام متكامل لإدارة المهام والصيانة ومراقبة الشبكة

### ✨ المميزات:

- ✅ واجهة عربية كاملة RTL
- ✅ تصميم احترافي حديث
- ✅ دعم الوضع الليلي
- ✅ متوافق مع الجوال والكمبيوتر
- ✅ نظام تسجيل دخول آمن
- ✅ صلاحيات متعددة (مدير، مشرف، فني)
- ✅ سجل تدقيق كامل
- ✅ تكامل Telegram
- ✅ تكامل MikroTik
- ✅ تقارير متقدمة (PDF, Excel, CSV)

### 👥 الأدوار والصلاحيات:

1. **مدير النظام** - إدارة كاملة للنظام
2. **المشرف** - إنشاء وتعديل المهام
3. **الفني** - تنفيذ وتحديث المهام

### 🚀 البدء السريع:

```bash
# استنساخ المستودع
git clone https://github.com/alsydd918-cmd/alcasbah-net.git
cd alcasbah-net

# إنشاء البيئة الافتراضية
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# تثبيت المتطلبات
pip install -r requirements.txt

# نسخ ملف الإعدادات
cp .env.example .env

# تهيئة قاعدة البيانات
python init_db.py

# تشغيل التطبيق
python app.py
```

### 📊 بيانات تسجيل الدخول التجريبية:

| الدور | المستخدم | كلمة المرور |
|------|---------|----------|
| مدير | admin | admin123 |
| مشرف | supervisor | supervisor123 |
| فني | tech1 | tech123 |

### 🐳 التشغيل مع Docker:

```bash
docker-compose up -d
```

### 📁 هيكل المشروع:

```
alcasbah-net/
├── app/
│   ├── models.py          # نماذج قاعدة البيانات
│   ├── routes/            # المسارات والواجهات
│   ├── services/          # الخدمات
│   ├── templates/         # القوالب HTML
│   └── static/            # الملفات الثابتة
├── config.py              # الإعدادات
├── app.py                 # تطبيق Flask
├── requirements.txt       # المتطلبات
└── docker-compose.yml     # Docker Compose
```

### 🔐 الأمان:

- تشفير كلمات المرور بـ bcrypt
- حماية CSRF
- JWT Authentication
- Rate Limiting
- Session Management
- Activity Logs

### 📱 المتوافقة:

- Windows, Linux, macOS
- Chrome, Firefox, Safari, Edge
- الأجهزة المحمولة

### 🤝 المساهمة:

نرحب بمساهماتك! يرجى فتح Issue أو Pull Request.

### 📄 الترخيص:

MIT License

### 📞 التواصل:

- Email: info@alcasbah.net
- GitHub: https://github.com/alsydd918-cmd/alcasbah-net
