import requests

JUDGE0_URL = "http://localhost:2358/submissions/?base64_encoded=false&wait=true"

# O'quvchi yozgan kod
student_code = """
a, b = map(int, input().split())
print(a + b)
"""

# Test ma'lumotlari
input_data = "2 3\n"
expected_output = "5\n"

# Judge0 ga yuborish
data = {
    "language_id": 71,   # Python 3
    "source_code": student_code,
    "stdin": input_data,
    "cpu_time_limit": 2,   # 2 sekund limit
    "memory_limit": 1024   # MB
}

res = requests.post(JUDGE0_URL, json=data)
result = res.json()

status_id = result["status"]["id"]
status_desc = result["status"]["description"]

print("🔍 Status:", status_desc)

# Tekshirish
if status_id == 3:  # Accepted
    if result["stdout"] == expected_output:
        print("✅ To‘g‘ri javob")
    else:
        print("❌ Xato javob")
        print("Chiqqan:", result["stdout"])
        print("Kutilgan:", expected_output)
elif status_id == 5:
    print("⏱ Vaqt limiti oshib ketdi (Time Limit Exceeded)")
elif status_id == 6:
    print("🛠 Kompilyatsiya xatosi")
    print(result.get("compile_output"))
elif status_id == 7:
    print("⚡ Runtime xato")
    print(result.get("stderr"))
else:
    print("❌ Boshqa xato:", status_desc)
