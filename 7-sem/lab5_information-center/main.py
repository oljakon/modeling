import numpy.random as rn


class RandomGenerator:
    def __init__(self, begin, delta=0):
        self.begin = begin
        self.d = delta

    def new_random(self):
        if (self.d == 0):
            return self.begin
        return rn.uniform(self.begin - self.d, self.begin + self.d)


class GenerateRequest:
    def __init__(self, generator, count):
        self.random_generator = generator
        self.num_requests = count
        self.receivers = []
        self.next = 0

    def generate_request(self):
        self.num_requests -= 1
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        return self.random_generator.new_random()


class ProcessRequest:
    def __init__(self, generator, max_queue_size=-1):
        self.random_generator = generator
        self.queue, self.received, self.max_queue, self.processed = 0, 0, max_queue_size, 0
        self.next = 0

    def receive_request(self):
        if self.max_queue == -1 or self.max_queue > self.queue:
            self.queue += 1
            self.received += 1
            return True
        return False

    def process_request(self):
        if self.queue > 0:
            self.queue -= 1
            self.processed += 1

    def delay(self):
        return self.random_generator.new_random()


class Model:
    def __init__(self, generator, operators, computers):
        self.generator = generator
        self.operators = operators
        self.computers = computers

    def event_mode(self):
        refusals = 0
        generated_requests = self.generator.num_requests
        generator = self.generator

        generator.receivers = [self.operators[0], self.operators[1], self.operators[2]]
        self.operators[0].receivers = [self.computers[0]]
        self.operators[1].receivers = [self.computers[0]]
        self.operators[2].receivers = [self.computers[1]]

        generator.next = generator.delay()
        self.operators[0].next = self.operators[0].delay()

        blocks = [generator,
                  self.operators[0],
                  self.operators[1],
                  self.operators[2],
                  self.computers[0],
                  self.computers[1]]

        while generator.num_requests >= 0:
            current_time = generator.next
            for block in blocks:
                if 0 < block.next < current_time:
                    current_time = block.next

            for block in blocks:
                if current_time == block.next:
                    if not isinstance(block, ProcessRequest):
                        next_generator = generator.generate_request()
                        if next_generator is not None:
                            next_generator.next = current_time + next_generator.delay()
                        else:
                            refusals += 1
                        generator.next = current_time + generator.delay()
                    else:
                        block.process_request()
                        if block.queue == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.delay()

        return {"refusal_percentage": refusals / generated_requests * 100,
                "refusals": refusals}


if __name__ == '__main__':
    min_p = 100
    max_p = 0
    min_r = 300
    max_r = 0

    for i in range(100):
        time_clients = 10
        delta_time_clients = 2

        first_operator = 20
        second_operator = 40
        third_operator = 40

        first_computer = 15
        second_computer = 30

        delta_first_operators = 5
        delta_second_operators = 10
        delta_third_operators = 20

        clients_number = 300

        generator = GenerateRequest(RandomGenerator(time_clients, delta_time_clients), clients_number)
        operators = [ProcessRequest(RandomGenerator(first_operator, delta_first_operators), max_queue_size=1),
                     ProcessRequest(RandomGenerator(second_operator, delta_second_operators), max_queue_size=1),
                     ProcessRequest(RandomGenerator(third_operator, delta_third_operators), max_queue_size=1)]
        computers = [ProcessRequest(RandomGenerator(first_computer)),
                      ProcessRequest(RandomGenerator(second_computer))]

        model = Model(generator, operators, computers)
        result = model.event_mode()

        if (min_p >= result['refusal_percentage']):
            min_p = result['refusal_percentage']
        if (max_p <= result['refusal_percentage']):
            max_p = result['refusal_percentage']
        if (min_r >= result['refusals']):
            min_r = result['refusals']
        if (max_r <= result['refusals']):
            max_r = result['refusals']

    print("Событийная модель: ")
    print(f"Количество отказов: [{min_r}; {max_r}]")
    print(f"Процент отказов в обработке: [{round(min_p, 4)}; {round(max_p, 4)}]")