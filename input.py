patterns = [
    "AAAAAAAAAAAAAAAAAAAAAA",  
    "BBBBBBBBBBBBBBBBBBBBBB",  
    "CCCCCCCCCCCCCCCCCCCCCC",  
    "DDDDDDDDDDDDDDDDDDDDDD",  
    "EEEEEEEEEEEEEEEEEEEEEE",  
    "FFFFFFFFFFFFFFFFFFFFFF",  
    "GGGGGGGGGGGGGGGGGGGGGG",  
]

with open("test_files/input.txt", "w", encoding="utf-8") as f:
    for _ in range(20000):  
        for p in patterns:
            f.write(p)
        f.write("\n")
