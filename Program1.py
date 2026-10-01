def main():
    try:
        n, k, m = map(int, input().split())
        students = []

        for i in range(n):
            data = input().split()
            enrollment = data[0]
            name = data[1]
            semester = int(data[2])
            cpi = float(data[3])
            marks = list(map(int, data[4:]))

            student = {
                "enrollment": enrollment,
                "name": name,
                "semester": semester,
                "cpi": cpi,
                "marks": marks,
                "average": sum(marks) / len(marks)
            }
            students.append(student)

        semesters = {}
        for student in students:
            sem = student["semester"]
            if sem not in semesters:
                semesters[sem] = []
            semesters[sem].append(student)

        for sem in sorted(semesters):
            students_list = semesters[sem]
            students_list.sort(
                key=lambda x: (-x["cpi"], -x["average"], x["enrollment"])
            )
            result = [x["enrollment"] for x in students_list[:k]]
            print("Semester", sem, ":", " ".join(result))

        for j in range(m):
            highest = max(student["marks"][j] for student in students)
            toppers = []
            for student in students:
                if student["marks"][j] == highest:
                    toppers.append(student["enrollment"])
            toppers.sort()
            print("S" + str(j + 1) + ":", " ".join(toppers))

    except Exception:
        print("INVALID")


if __name__ == "__main__":
    main()
