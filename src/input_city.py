from datetime import datetime
print()
res = []
for i in range(24):
    res.append(f"{i}:00")
res = res[datetime.now().hour:]
print(res)
