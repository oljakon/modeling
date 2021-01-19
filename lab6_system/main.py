from numpy import random as nr
from random import shuffle


class RandomGenerator:
    def __init__(self, begin, delta=0):
        self.begin = begin
        self.d = delta

    def generate(self):
        if (self.d == 0):
            return self.begin
        return nr.uniform(self.begin - self.d, self.begin + self.d)


class GenerateRequest:
    def __init__(self, generator, name, count):
        self.random_generator = generator
        self.num_requests = count
        self.receivers = []
        self.next = 0
        self.name = name

    def generate_request(self):
        self.num_requests -= 1
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        return self.random_generator.generate()


class ProcessRequest:
    def __init__(self, generator, name, ban_probality=0, max_queue_size=-1, end=False):
        self.random_generator = generator
        self.queue = 0
        self.received = 0
        self.max_queue = max_queue_size
        self.processed = 0
        self.next = 0
        self.receivers = []
        self.end = end
        self.name = name
        self.ban_probality = ban_probality

    def receive_request(self):
        if self.max_queue == -1 or self.max_queue > self.queue:
            self.queue += 1
            self.received += 1
            return True
        return False

    def process_request(self):
        if nr.sample() < self.ban_probality:
            return "ban"
        if self.queue > 0:
            self.queue -= 1
            self.processed += 1
        shuffle(self.receivers)
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        return self.random_generator.generate()


class Model:
    def __init__(self, clients, terminals, office, cabinets):
        self.clients = clients
        self.terminals = terminals
        self.office = office
        self.cabinets = cabinets

    def event_mode(self):
        clients = self.clients

        clients.receivers = self.terminals.copy()
        self.terminals[0].receivers = [self.office, self.cabinets[2], self.cabinets[3]]
        self.terminals[1].receivers = [self.office, self.cabinets[2], self.cabinets[3]]
        self.terminals[2].receivers = [self.office, self.cabinets[2], self.cabinets[3]]
        self.office.receivers = [self.cabinets[0], self.cabinets[1]]

        clients.next = clients.delay()
        self.terminals[0].next = self.terminals[0].delay()
        '''self.terminals[1].next = self.terminals[1].delay()
        self.terminals[2].next = self.terminals[2].delay()'''

        blocks = []
        blocks += [clients]
        blocks += self.terminals
        blocks += [self.office]
        blocks += self.cabinets

        refusals = {}
        for block in blocks:
            refusals[block.name] = 0

        while clients.num_requests >= 0:
            current_time = clients.next
            for block in blocks:
                if 0 < block.next < current_time:
                    current_time = block.next

            for block in blocks:
                if current_time == block.next:
                    if not isinstance(block, ProcessRequest):
                        next_clients = clients.generate_request()

                        if next_clients is not None:
                            next_clients.next = current_time + next_clients.delay()
                        else:
                            refusals[block.name] += 1
                        clients.next = current_time + clients.delay()
                    else:
                        next_process = block.process_request()
                        if block.queue == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.delay()

                        if next_process == "ban":
                            refusals[block.name] += 1
                            continue

                        if block.end:
                            continue

                        if next_process is not None:
                            next_process.next = \
                                current_time + next_process.delay()
                        else:
                            refusals[block.name] += 1

        return refusals


def main():
    clients_number = 10000

    clients = GenerateRequest(RandomGenerator(3, 2), "entry", clients_number)

    terminals = [
        ProcessRequest(RandomGenerator(5, 2), "terminal1", 0.2, max_queue_size=3),
        ProcessRequest(RandomGenerator(5, 2), "terminal2", 0.2, max_queue_size=3),
        ProcessRequest(RandomGenerator(5, 2), "terminal3", 0.2, max_queue_size=3),
    ]

    office = ProcessRequest(RandomGenerator(10, 5), "office", 0.3, max_queue_size=5, end=False)

    cabinets = [
        ProcessRequest(RandomGenerator(6, 3), "cabinet1", 0.05, end=True),
        ProcessRequest(RandomGenerator(6, 3), "cabinet2", 0.05, end=True),
        ProcessRequest(RandomGenerator(8, 4), "cabinet3", 0.1, max_queue_size=10, end=True),
        ProcessRequest(RandomGenerator(20, 10), "cabinet4", 0.1, max_queue_size=10, end=True),
        #ProcessRequest(RandomGenerator(20, 10), "cabinet5", 0.1, max_queue_size=10, end=True)
    ]

    model = Model(clients, terminals, office, cabinets)
    result = model.event_mode()

    #print(result)
    print()
    print('Количество отказов:')
    print('Терминал 1: %d' % (result['terminal1']))
    print('Терминал 2: %d' % (result['terminal2']))
    print('Терминал 3: %d' % (result['terminal3']))
    print('Кабинет МВД: %d' % (result['office']))
    print('Кабинет 1: %d' % (result['cabinet1']))
    print('Кабинет 2: %d' % (result['cabinet2']))
    print('Кабинет 3: %d' % (result['cabinet3']))
    print('Кабинет 4: %d' % (result['cabinet4']))
    #print('Кабинет 5: %d' % (result['cabinet5']))

if __name__ == "__main__":
    main()
