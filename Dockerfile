# تحديد الصورة الأساسية لـ Python
FROM python:3.10-slim
# Cache Buster: This is a new deploy attempt.
# تعيين مجلد العمل
WORKDIR /usr/src/app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات التطبيق
COPY . .

# تحديد أمر تشغيل التطبيق
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app