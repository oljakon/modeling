import numpy.random as nr


class UniformGenerator:
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def generation_time(self):
        return nr.uniform(self._a, self._b)


class ErlangGenerator:
    def __init__(self, k, lmbd):
        self.k = k
        self.lmbd = lmbd

    def generation_time(self):
        return nr.gamma(self.k, self.lmbd)


class RequestGenerator:
    def __init__(self, generator):
        self._generator = generator
        self._receivers = set()

    def add_receiver(self, receiver):
        self._receivers.add(receiver)

    def remove_receiver(self, receiver):
        try:
            self._receivers.remove(receiver)
        except KeyError:
            pass

    def next_time_period(self):
        return self._generator.generation_time()

    def emit_request(self):
        for receiver in self._receivers:
            receiver.receive_request()


class RequestProcessor():
    def __init__(self, generator, reenter_probability=0):
        self._generator = generator
        self._current_queue_size = 0
        self._max_queue_size = 0
        self._processed_requests = 0
        self._reenter_probability = reenter_probability
        self._reentered_requests = 0

    @property
    def processed_requests(self):
        return self._processed_requests

    @property
    def max_queue_size(self):
        return self._max_queue_size

    @property
    def current_queue_size(self):
        return self._current_queue_size

    @property
    def reentered_requests(self):
        return self._reentered_requests

    def process(self):
        if self._current_queue_size > 0:
            self._processed_requests += 1
            self._current_queue_size -= 1
            if nr.random_sample() < self._reenter_probability:
                self._reentered_requests += 1
                self.receive_request()

    def receive_request(self):
        self._current_queue_size += 1
        if self._current_queue_size > self._max_queue_size:
            self._max_queue_size += 1

    def next_time_period(self):
        return self._generator.generation_time()


class Modeller:
    def __init__(self, generator, processor):
        self._generator = generator
        self._processor = processor
        self._generator.add_receiver(self._processor)

    def event_based_modelling(self, request_count):
        generator = self._generator
        processor = self._processor

        gen_period = generator.next_time_period()
        proc_period = gen_period + processor.next_time_period()
        while processor.processed_requests < request_count:
            if gen_period <= proc_period:
                generator.emit_request()
                gen_period += generator.next_time_period()
            else:
                processor.process()
                if processor.current_queue_size > 0:
                    proc_period += processor.next_time_period()
                else:
                    proc_period = gen_period + processor.next_time_period()

        result = [processor.processed_requests, processor.reentered_requests, processor.max_queue_size, proc_period]
        return result

    def time_based_modelling(self, request_count, dt):
        generator = self._generator
        processor = self._processor

        gen_period = generator.next_time_period()
        proc_period = gen_period + processor.next_time_period()
        current_time = 0
        while processor.processed_requests < request_count:
            if gen_period <= current_time:
                generator.emit_request()
                gen_period += generator.next_time_period()
            if current_time >= proc_period:
                processor.process()
                if processor.current_queue_size > 0:
                    proc_period += processor.next_time_period()
                else:
                    proc_period = gen_period + processor.next_time_period()
            current_time += dt

        result = [processor.processed_requests, processor.reentered_requests, processor.max_queue_size, current_time]
        return result


if __name__ == "__main__":
    a = 1
    b = 10

    k = 9
    lmbd = 0.5

    total_apps = 10000
    reenter = 1
    step = 1

    generator = RequestGenerator(UniformGenerator(a, b))
    processor = RequestProcessor(ErlangGenerator(k, lmbd), reenter)
    model = Modeller(generator, processor)
    result_tb = model.time_based_modelling(total_apps, step)
    print("Принцип delta t:")
    print("Обработанные заявки: ", result_tb[0])
    print("Повторно обработанные заявки: ", result_tb[1])
    print("Длина очереди: ", result_tb[2])

    generator = RequestGenerator(UniformGenerator(a, b))
    processor = RequestProcessor(ErlangGenerator(k, lmbd), reenter)
    model = Modeller(generator, processor)
    result_eb = model.event_based_modelling(total_apps)
    print("\nСобытийный принцип:")
    print("Обработанные заявки: ", result_eb[0])
    print("Повторно обработанные заявки: ", result_eb[1])
    print("Длина очереди: ", result_eb[2])

