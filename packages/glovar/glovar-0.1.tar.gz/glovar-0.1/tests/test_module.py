import glovar

print(glovar.get("x"))
for i in range(10):
    glovar.set("x", glovar.get("x") + 1)
    print(glovar.get("x"))