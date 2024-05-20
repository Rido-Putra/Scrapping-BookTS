'''
1. Membuat list daftar_nama yang berisi nama-nama teman.
2. Membuat dictionary data_temans yang berisi informasi tentang teman-teman.
3. Menampilkan nama-nama teman dari list daftar_nama.
4. Menampilkan informasi lengkap teman pertama dari dictionary data_temans.
5. Menampilkan hanya usia teman kedua dari dictionary data_temans.
6. Menambahkan teman baru ke dalam list daftar_nama dan dictionary data_temans.
7. Menghapus teman pertama dari list daftar_nama dan dictionary data_temans.
8. Menampilkan nama-nama teman setelah perubahan.'''

# 1. Membuat list daftar_nama yang berisi nama-nama teman.
friend_lists = ["Budi", "Ani", "Badu"]
# 2. Membuat dictionary data_temans yang berisi informasi tentang teman-teman.
friend_data = {"Budi" : {"age" : 25, "hobby" : "fishing"},
               "Ani" : {"age" : 26, "hobby" : "hiking"},
               "Badu" : {"age" :27, "hobby" : "hijacking"}}
# 3. Menampilkan nama-nama teman dari list daftar_nama.
print(friend_lists)
for friend in friend_lists:
    print(friend)
# 4. Menampilkan informasi lengkap teman pertama dari dictionary data_temans.
first_friend = friend_lists[0]
print(f"First friend detail information, name : {first_friend}, {friend_data[first_friend]}")
# 5. Menampilkan hanya usia teman kedua dari dictionary data_temans.
second_friend = friend_lists[1]
second_friend_age = friend_data[second_friend]["age"]
# 6. Menambahkan teman baru ke dalam list daftar_nama dan dictionary data_temans.
new_friend = "Jono"
friend_lists.append(new_friend)
friend_data[new_friend] = {"age" : 29, "hobby" : "running"}
# 7. Menghapus teman pertama dari list daftar_nama dan dictionary data_temans.
delete_friend = friend_lists.pop(0)
del friend_data[delete_friend]
# 8. Menampilkan nama-nama teman setelah perubahan.
print(f"New update friend list {friend_lists}")
print(f"New update friend detail information {friend_data}")

#1. Iterasi melalui kunci-kunci dictionary
print("Iteration through dictionary keys")
for name in friend_data:
    print(name)
#2. Iterasi melalui nilai-nilai dictionary
print("Iteration through dictionary values")
for info in friend_data.values():
    print(info)
#3. Iterqasi melalui kunci dan nilai dictionary
print("Iteration through dictionary keys and values")
for name, info in friend_data.items():
    print(f"Name : {name}, Age : {info['age']}, Hobby : {info['hobby']}")