import heapq


def main():
    try:
        w, n = map(int, input().split())
        jobs = []

        for i in range(n):
            arrival, job_id, priority, duration, resources = input().split()

            job = (
                int(arrival),
                job_id,
                int(priority),
                int(duration),
                int(resources),
                i
            )
            jobs.append(job)

        jobs.sort(key=lambda x: (x[0], x[5]))

        workers = []
        for i in range(1, w + 1):
            heapq.heappush(workers, (0, i))

        waiting = []
        index = 0
        result = []

        while index < n or waiting:
            if not waiting:
                current_time = max(
                    jobs[index][0],
                    workers[0][0]
                )
            else:
                current_time = workers[0][0]

            while index < n and jobs[index][0] <= current_time:
                job = jobs[index]
                heapq.heappush(
                    waiting,
                    (-job[2], job[0], job[5], job)
                )
                index += 1

            if not waiting:
                continue

            free_time, worker = heapq.heappop(workers)
            job = heapq.heappop(waiting)[3]

            start = max(free_time, job[0])
            finish = start + job[3]

            result.append((job, worker, start, finish))
            heapq.heappush(workers, (finish, worker))

        result.sort(key=lambda x: (x[2], x[1]))

        total_wait = 0

        for job, worker, start, finish in result:
            total_wait += start - job[0]
            print(job[1], "W" + str(worker), start, finish)

        print("AVG_WAIT", format(total_wait / n, ".2f"))

    except Exception:
        print("INVALID")


if __name__ == "__main__":
    main()
