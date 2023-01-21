# Mein erstes Programm, das ist ein Kommentar

print("Hallo Welt!")

name = input("Wie heisst Du? ")

if name:             # if not name == "":
	print("Hallo {}!".format(name))
else:
	print("Du hast keinen Namen.")
