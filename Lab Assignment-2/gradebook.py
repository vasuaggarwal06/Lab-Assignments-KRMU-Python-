import csv

print("Welcome to GradeBook")

while True:
    print("\n1. Add Data")
    print("2. Show Data")
    print("3. Exit")
    ch = input("Enter your choice: ")

    if ch == "1":
        data = []
        while True:
            name = input("\nEnter student name (or 'done' to stop): ")
            if name.lower() == "done":
                break

            m1 = float(input("Marks in Subject 1: "))
            m2 = float(input("Marks in Subject 2: "))
            m3 = float(input("Marks in Subject 3: "))
            m4 = float(input("Marks in Subject 4: "))

            avg = (m1 + m2 + m3 + m4) / 4

            if avg >= 90:
                g = "A"
            elif avg >= 80:
                g = "B"
            elif avg >= 70:
                g = "C"
            elif avg >= 60:
                g = "D"
            else:
                g = "F"

            data.append([name, m1, m2, m3, m4, avg, g])

       
        print("\n==============================================")
        print("Name\tSub1\tSub2\tSub3\tSub4\tAvg\tGrade")
        print("==============================================")
        for s in data:
            print(f"{s[0]}\t{s[1]}\t{s[2]}\t{s[3]}\t{s[4]}\t{s[5]:.2f}\t{s[6]}")
        print("==============================================")

        f = open("marks.csv", "a", newline="")
        w = csv.writer(f)
        for s in data:
            w.writerow(s)
        f.close()
        print("\nSaved to marks.csv")

    elif ch == "2":
        try:
            f = open("marks.csv")
            r = csv.reader(f)
            rows = list(r)
            if len(rows) == 0:
                print("\nNo data found!")
            else:
                print("\n==============================================")
                print("Name\tSub1\tSub2\tSub3\tSub4\tAvg\tGrade")
                print("==============================================")
                for s in rows:
                    print(f"{s[0]}\t{s[1]}\t{s[2]}\t{s[3]}\t{s[4]}\t{s[5]}\t{s[6]}")
                print("==============================================")
            f.close()
        except:
            print("\nFile not found!")

    elif ch == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
